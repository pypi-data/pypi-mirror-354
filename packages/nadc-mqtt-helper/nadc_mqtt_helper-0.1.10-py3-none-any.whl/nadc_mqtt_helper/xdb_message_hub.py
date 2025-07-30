import paho.mqtt.client as mqtt
import json
import time
import threading
import logging
import uuid
from typing import Callable
from .models import TelescopeStatusInfo, ObservationData
logger = logging.getLogger(__name__)

TOPIC_ALERT_FOLLOWUP = "TDIC/Alert/Followup"
TOPIC_TELESCOPE_ALERT_FOLLOWUP = "TDIC/Alert/{telescope_tid}/Followup"
TOPIC_SCHEDULE = "GWOPS/{telescope_tid}/schedule"

TOPIC_STATUS_UPDATE = "GWOPS/{telescope_tid}/status_update"
TOPIC_DATA = "GWOPS/{telescope_tid}/data"
TOPIC_OBSERVED = "GWOPS/{telescope_tid}/observed"

class TelescopeClient:
    def __init__(self, tid, password, host, port):
        self.tid = tid  # 保存原始的telescope ID
        self.password = password
        self.host = host
        self.port = port

        self.on_public_alert = None
        self.on_private_alert = None
        self.on_schedule = None

        # 使用 tid + 随机UUID 确保客户端ID唯一性
        self.client_id = f"{tid}-{str(uuid.uuid4())[:8]}"
        logger.info(f"create mqtt client - TID: {tid}, Client ID: {self.client_id}")
        
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.username_pw_set(tid, password)  # 认证仍使用原始tid
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        # 添加断开连接回调
        self.client.on_disconnect = self._on_disconnect

    def connect(self, start_loop=True):
        """
        连接到MQTT代理
        :param start_loop: 是否自动启动消息循环（使用loop_start）
        """
        self.client.connect(self.host, self.port, 60)
        if start_loop:
            self.client.loop_start()
            
    def loop_forever(self):
        """
        在当前线程中启动消息循环，会阻塞当前线程
        """
        self.client.loop_forever()
        
    def loop_start(self):
        """
        在后台线程中启动消息循环，不会阻塞当前线程
        """
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()   
        self.client.disconnect()

    def get_telescope_id(self):
        """获取原始的望远镜ID"""
        return self.tid
    
    def get_client_id(self):
        """获取MQTT客户端ID"""
        return self.client_id
    
    def get_connection_info(self):
        """获取连接信息"""
        return {
            'telescope_id': self.tid,
            'client_id': self.client_id,
            'host': self.host,
            'port': self.port
        }

    def subscribe_to_public_alerts(self, callback: Callable):
        """Subscribe to GCN alert broadcast topic"""
        self.client.subscribe(TOPIC_ALERT_FOLLOWUP, qos=1)
        self.on_public_alert = callback

    def subscribe_to_private_alerts(self, callback: Callable):
        """Subscribe to telescope-specific alerts"""
        topic = TOPIC_TELESCOPE_ALERT_FOLLOWUP.format(telescope_tid=self.tid)
        self.client.subscribe(topic, qos=1)
        self.on_private_alert = callback

    def subscribe_to_schedule(self, callback: Callable):
        """Subscribe to telescope-specific observation schedule (GW observation fields or targets)"""
        topic = TOPIC_SCHEDULE.format(telescope_tid=self.tid)
        self.client.subscribe(topic, qos=1)
        self.on_schedule = callback

    def publish_status(self, status_data: TelescopeStatusInfo):
        """
        Publish detailed telescope status information
        """
        topic = TOPIC_STATUS_UPDATE.format(telescope_tid=self.tid)
        message = json.dumps(status_data.to_dict())
        self.client.publish(topic, message, qos=1)
  
    def publish_observation(self, observation_data: ObservationData):
        """
        Publish observation execution status
        """
        topic = TOPIC_OBSERVED.format(telescope_tid=self.tid)
        message = json.dumps(observation_data.to_dict())
        self.client.publish(topic, message, qos=1)

    def publish_data(self, event_name, data):
        """
        Publish observation data
        :param event_name: Alert ID
        :param data: Observation data, can be small data content or URL link to large data
        """
        topic = TOPIC_DATA.format(telescope_tid=self.tid)
        message = json.dumps({
            "event_name": event_name,
            "data": data
        })
        self.client.publish(topic, message, qos=1)

    def start_publish_status_timer(self, interval, fetch_new_status: Callable):
        """
        Start periodic status publishing

        :param interval: Publishing interval in seconds
        :param fetch_new_status: Function to fetch new status data
        """
        def timer_func():
            while True:
                status_data = fetch_new_status()
                self.publish_status(status_data)  # Update status as needed
                time.sleep(interval)

        thread = threading.Thread(target=timer_func)
        thread.daemon = True  # Set as daemon thread, exits with main program
        thread.start()

    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connection is established"""
        if rc == 0:
            logger.info(f"Successfully connected to MQTT broker (Client ID: {self.client_id})!")
            logger.info(f"Connection flags: {flags}")
        else:
            error_messages = {
                1: "connection refused - protocol version incorrect",
                2: "connection refused - client identifier invalid", 
                3: "connection refused - server unavailable",
                4: "connection refused - username or password incorrect",
                5: "connection refused - not authorized"
            }
            error_msg = error_messages.get(rc, f"connection failed with return code: {rc}")
            logger.error(f"Connection failed with return code: {rc} - {error_msg}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback when connection is lost"""
        if rc != 0:
            logger.warning(f"unexpected disconnection (Client ID: {self.client_id}, return code: {rc})")
            logger.warning("client will try to reconnect...")
        else:
            logger.info(f"normal disconnection (Client ID: {self.client_id})")

    def _on_message(self, client, userdata, msg):
        """Callback when message is received"""
        try:
            topic_private_alert = TOPIC_TELESCOPE_ALERT_FOLLOWUP.format(telescope_tid=self.tid)
            topic_public_alert = TOPIC_ALERT_FOLLOWUP
            topic_schedule = TOPIC_SCHEDULE.format(telescope_tid=self.tid)

            payload = msg.payload.decode("utf-8")
            logger.debug(f"Received message on topic: {msg.topic}")
            
            if msg.topic == topic_public_alert and self.on_public_alert:
                try:
                    self.on_public_alert(payload)
                except Exception as e:
                    logger.error(f"Error in public alert callback: {e}")
            elif msg.topic == topic_private_alert and self.on_private_alert:
                try:
                    self.on_private_alert(payload)
                except Exception as e:
                    logger.error(f"Error in private alert callback: {e}")
            elif msg.topic == topic_schedule and self.on_schedule:
                try:
                    self.on_schedule(payload)
                except Exception as e:
                    logger.error(f"Error in schedule callback: {e}")
        except UnicodeDecodeError as e:
            logger.error(f"Failed to decode message payload: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in message handling: {e}")