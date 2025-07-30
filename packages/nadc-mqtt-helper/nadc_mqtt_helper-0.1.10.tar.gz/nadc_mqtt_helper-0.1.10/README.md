## NADC MQTT Helper

This library encapsulates MQTT client tools for communication and data exchange between telescopes and the NADC platform.

### Installation

```bash
pip install nadc-mqtt-helper
```

### Main Features

- Subscribe: Platform broadcasts alert information to telescopes, corresponding to the topic "TDIC/Alert/Followup"
- Subscribe: Platform sends private alert information to specific telescopes, corresponding to the topic "TDIC/Alert/<telescope TID>/Followup", used for sending non-public EP SVOM alerts to specific telescopes
- Subscribe: Platform sends observation planning information to telescopes, corresponding to the topic "GWOPS/<telescope TID>/schedule", currently mainly for gravitational wave event observation planning
- Publish: Telescopes send status information to the platform, corresponding to the topic "GWOPS/<telescope TID>/status_update"
- Publish: Telescopes send observation status information to the platform, corresponding to the topic "GWOPS/<telescope TID>/observed"
- Publish: Telescopes provide observation data to the platform, corresponding to the topic "GWOPS/<telescope TID>/data"

### Basic Usage

#### Create and Connect Client

```python
from nadc_mqtt_helper.xdb_message_hub import TelescopeClient
from nadc_mqtt_helper.models import TelescopeStatusInfo, ObservationData

# Create client connection
client = TelescopeClient(
    tid="your_telescope_id",
    password="your_password",
    host="39.105.33.247",
    port=5673
)

# Connect to MQTT server
client.connect()

# Disconnect when finished
client.disconnect()

# Note: If your program is not a long-running process, you need to use client's loop_forever function instead of loop_start

# Step 1: Disable loop_start during connection. loop_start creates background thread listening, which is suitable for resident processes like web servers
client.connect(start_loop=False)

# Step 2: Implement subscription logic here. Place message handling and subscription initialization after connection
client.subscribe_to_public_alerts(handle_public_alert)

# Step 3: Maintain persistent operation. loop_forever blocks main thread to keep program running for continuous message reception
client.loop_forever()
```


#### Subscribe to Messages

```python
# Subscribe to public alerts
def handle_public_alert(payload):
    print(f"Received public alert, processing: {payload}")

client.subscribe_to_public_alerts(handle_public_alert)

# Subscribe to private alerts
def handle_private_alert(payload):
    print(f"Received private alert, processing: {payload}")

client.subscribe_to_private_alerts(handle_private_alert)

# Subscribe to scheduling information
def handle_schedule(payload):
    print(f"Received scheduling information, processing: {payload}")

client.subscribe_to_schedule(handle_schedule)
```

#### Publish Telescope Status

```python
from nadc_mqtt_helper.models import EnvironmentData, TelescopeStatus, TelescopeStatusInfo
from datetime import datetime

# Create environment data
env_data = EnvironmentData(
    time=datetime.now(),
    temperature=15.5,
    humidity=45.0,
    dewtemperature=5.2,
    pressure=1013.0,
    height=100.0,
    windspeed=5.0,
    windspeed_2=6.0,
    windspeed_10=7.0,
    windDirection=270,
    Rainfall=0.0,
    Rainfall_all=10.0,
    pm25=15.0,
    pm10=30.0,
    voltage=220.0,
    TimeStamp=datetime.now()
)

# Create telescope status
telescope_status = TelescopeStatus(
    telescope="2.4m",
    instrument="CCD",
    observation_assistant="someone",
    assistant_telephone="12345678901",
    status="observing",
    is_observable=True,
    daytime="night",
    too_observing="available",
    date=datetime.now()
)

# Create telescope status information
status_info = TelescopeStatusInfo(
    environment=[env_data],
    telescope_status=telescope_status
)

# Publish status
client.publish_status(status_info)
```

#### Publish Observation Data

```python
from nadc_mqtt_helper.models import ObservationData
from datetime import datetime, timedelta

# Create observation data
now = datetime.now()
observation = ObservationData(
    telescope="2.4m",
    Instrument="YFOSC",
    pointing_ra=83.8221,
    pointing_dec=-5.3911,
    start_time=now,
    end_time=now + timedelta(minutes=30),
    duration=30.0,
    event_name="M42",
    observer="someone",
    obs_type="science",
    comment="for testing",
    update_time=now
)

# Publish observation data
client.publish_observation(observation)
```

### Data Models

The library provides the following main data models:

1. `EnvironmentData`: Environmental data model, containing environmental parameters such as temperature, humidity, pressure, etc.
2. `TelescopeStatus`: Telescope status model, containing the current working status of the telescope
3. `TelescopeStatusInfo`: Telescope information model, containing environmental data and telescope status
4. `ObservationData`: Observation data model, recording observation details

#### Data Model Field Details

##### EnvironmentData Model

| Field | Type | Example | Description |
|------|------|-------|-----|
| time | datetime | 2023-05-20T18:30:00 | Data recording time |
| temperature | float | 15.5 | Temperature (°C) |
| humidity | float | 45.0 | Humidity (%) |
| dewtemperature | float | 5.2 | Dew point temperature (°C) |
| pressure | float | 1013.0 | Atmospheric pressure (hPa) |
| height | float | 100.0 | Height (m) |
| windspeed | float | 5.0 | Wind speed (m/s) |
| windspeed_2 | float | 6.0 | Wind speed at 2m height (m/s) |
| windspeed_10 | float | 7.0 | Wind speed at 10m height (m/s) |
| windDirection | int | 270 | Wind direction (degrees) |
| Rainfall | float | 0.0 | Rainfall (mm) |
| Rainfall_all | float | 10.0 | Total rainfall (mm) |
| pm25 | float | 15.0 | PM2.5 concentration (μg/m³) |
| pm10 | float | 30.0 | PM10 concentration (μg/m³) |
| voltage | float | 220.0 | Voltage (V) |
| TimeStamp | datetime | 2023-05-20T18:30:00 | Timestamp |

##### TelescopeStatus Model

| Field | Type | Example | Description |
|------|------|-------|-----|
| telescope | string | "2.4m" | Telescope identifier |
| instrument | string | "CCD" | Instrument in use |
| observation_assistant | string | "John Doe" | Name of observation assistant |
| assistant_telephone | string | "12345678901" | Assistant's contact phone |
| status | string | "observing" | Current telescope status |
| is_observable | bool | true | Whether observation is possible |
| daytime | string | "night" | Day/night status |
| too_observing | string | "available" | TOO observation status |
| date | datetime | 2023-05-20T18:30:00 | Record date |

##### TelescopeStatusInfo Model

| Field | Type | Description |
|------|------|-----|
| environment | List[EnvironmentData] | List of environmental data |
| telescope_status | TelescopeStatus | Telescope status information |

##### ObservationData Model

| Field | Type | Example | Description |
|------|------|-------|-----|
| telescope | string | "2.4m" | Telescope identifier |
| Instrument | string | "YFOSC" | Instrument in use |
| pointing_ra | float | 83.8221 | Right ascension (degrees) |
| pointing_dec | float | -5.3911 | Declination (degrees) |
| start_time | datetime | 2023-05-20T20:00:00 | Observation start time |
| end_time | datetime | 2023-05-20T20:30:00 | Observation end time |
| duration | float | 30.0 | Observation duration (minutes) |
| event_name | string | "M42" | Target name |
| observer | string | "Jane Smith" | Observer name |
| obs_type | string | "science" | Observation type |
| comment | string | "Orion Nebula observation" | Observation notes |
| update_time | datetime | 2023-05-20T20:30:00 | Data update time |

### Client Example

Refer to the `xdb_message_client.py` file for a complete client example code. 