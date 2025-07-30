from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List
from dateutil import parser

@dataclass
class EnvironmentData:
    time: datetime
    temperature: float
    humidity: float
    dewtemperature: float
    pressure: float
    height: float
    windspeed: float
    windspeed_2: float
    windspeed_10: float
    windDirection: int
    Rainfall: float
    Rainfall_all: float
    pm25: float
    pm10: float
    voltage: float
    TimeStamp: datetime

    @classmethod
    def from_dict(cls, data: dict):
        filtered_data = {k: v for k, v in data.items() if k in cls.__annotations__}
        if 'time' in filtered_data:
            filtered_data['time'] = parser.isoparse(filtered_data['time'])
        if 'TimeStamp' in filtered_data:
            filtered_data['TimeStamp'] = parser.isoparse(filtered_data['TimeStamp'])
            
        return cls(**filtered_data)

    def to_dict(self):
        data = asdict(self)
        data['time'] = self.time.isoformat()
        data['TimeStamp'] = self.TimeStamp.isoformat()
        return {k: v for k, v in data.items() if v is not None}

@dataclass
class TelescopeStatus:
    telescope: str
    instrument: str
    observation_assistant: str
    assistant_telephone: str
    status: str
    is_observable: bool
    daytime: str
    too_observing: str
    date: datetime

    @classmethod
    def from_dict(cls, data: dict):
        valid_fields = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        if isinstance(filtered_data.get('date'), str):
            filtered_data['date'] = parser.isoparse(filtered_data['date'])
            
        return cls(**filtered_data)

    def to_dict(self):
        data = asdict(self)
        data['date'] = self.date.isoformat()
        return {k: v for k, v in data.items() if v is not None} 

@dataclass
class TelescopeStatusInfo:
    environment: List[EnvironmentData]
    telescope_status: TelescopeStatus

    @classmethod
    def from_dict(cls, data: dict):
        env_data = [EnvironmentData.from_dict(item) for item in data.get('environment', [])]
        telescope_status = TelescopeStatus.from_dict(data.get('telescope_status', {}))
        return cls(
            environment=env_data,
            telescope_status=telescope_status
        )

    def to_dict(self):
        return {
            'environment': [env.to_dict() for env in self.environment],
            'telescope_status': self.telescope_status.to_dict()
        }

@dataclass
class ObservationData:
    telescope: str
    Instrument: str
    pointing_ra: float
    pointing_dec: float
    start_time: datetime
    end_time: datetime
    duration: float
    event_name: str
    observer: str
    obs_type: str
    comment: Optional[str] = None
    update_time: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict):
        valid_fields = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        time_fields = ['start_time', 'end_time', 'update_time']
        for field in time_fields:
            if isinstance(filtered_data.get(field), str):
                filtered_data[field] = parser.isoparse(filtered_data[field])
            
        return cls(**filtered_data)

    def to_dict(self):
        data = asdict(self)
        time_fields = ['start_time', 'end_time', 'update_time']
        for field in time_fields:
            if hasattr(self, field) and getattr(self, field) is not None:
                data[field] = getattr(self, field).isoformat()
        
        return {k: v for k, v in data.items() if v is not None} 