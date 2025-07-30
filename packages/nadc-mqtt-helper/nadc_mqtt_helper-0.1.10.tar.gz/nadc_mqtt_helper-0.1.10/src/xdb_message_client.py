# coding: utf-8

import logging
from nadc_mqtt_helper import TelescopeClient, EnvironmentData, TelescopeStatus, TelescopeStatusInfo, ObservationData
import time
from datetime import datetime


def handle_public_alert(payload):
    print("receive a public alert:", payload)

def handle_private_alert(payload):
    print("receive a private alert:", payload)

def handle_schedule(payload):
    print("receive a schedule:", payload)


client = TelescopeClient(
    tid="TID",
    password="xxxx",
    host="host",
    port=1111
)


client.connect(start_loop=False)

client.subscribe_to_public_alerts(handle_public_alert)
client.subscribe_to_private_alerts(handle_private_alert)
client.subscribe_to_schedule(handle_schedule)

# new_status = {"environment": [{"id": 619577, "time": "2025-02-28T12:27:01", "temperature": 14.9, "humidity": 16.3, "dewtemperature": -10.43, "pressure": 912.7, "height": 0.0, "windspeed": 0.3, "windspeed_2": 1.2, "windspeed_10": 1.5, "windDirection": 204, "Rainfall": 0.0, "Rainfall_all": 0.0, "pm25": 29.0, "pm10": 33.0, "voltage": 13.5, "TimeStamp": "2025-02-28T12:27:01"}], "telescope status": {"id": 30, "telescope": "XL080", "observation_assistant": "\u5f20\u91d1\u78ca", "assistant_telephone": "15231419229", "status": "online", "is_observable": True, "daytime": "day", "too_observing": "ToO_Level1", "date": "2025-02-25T18:52:01.756000+08:00"}}
# client.publish_status_update(new_status)

data_dict = {
    "environment": [
        {
            "id": 619607,
            "time": "2025-02-28T12:57:01",
            "temperature": 14.7,
            "humidity": 19.7,
            "dewtemperature": -8.19,
            "pressure": 912.3,
            "height": 0.0,
            "windspeed": 1.4,
            "windspeed_2": 1.8,
            "windspeed_10": 1.7,
            "windDirection": 132,
            "Rainfall": 0.0,
            "Rainfall_all": 0.0,
            "pm25": 51.0,
            "pm10": 57.0,
            "voltage": 13.5,
            "TimeStamp": "2025-02-28T12:57:01"
        }
    ],
    "telescope_status": {
        "id": 13,
        "telescope": "XL216",
        "instrument": "BFOSC",
        "observation_assistant": "柳森",
        "assistant_telephone": "1236582",
        "status": "online",
        "is_observable": True,
        "daytime": "day",
        "too_observing": "ToO_Level1",
        "date": "2024-12-26T15:07:07.001000+08:00"
    }
}

telescope_status_info = TelescopeStatusInfo.from_dict(data_dict)

client.publish_status(telescope_status_info)
print("publish status update done")


observation_data_dict = {
    'telescope': 'XL216',
    'Instrument': 'HRS',
    'pointing_ra': 211,
    'pointing_dec': 63,
    'start_time': '2024-08-21T16:34:24Z',
    'end_time': '2024-08-21T17:34:24Z',
    'duration': 1000,
    'event_name': 'EP240818a',
    'observer': 'Yunfei Xu',
    'obs_type': 'Spectrum',
    'comment': 'for testing',
    'update_time': '2024-08-21T17:35:24Z'
}

observation = ObservationData.from_dict(observation_data_dict)
client.publish_observation(observation)

print("publish observation data done")


client.publish_data('event', 'http://bac.dt')
print("publish data done")


# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     client.disconnect()
#     print("process exits")