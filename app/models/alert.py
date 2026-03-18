from datetime import datetime, timezone, timedelta
from typing import Optional

from pydantic import BaseModel, field_validator

ISRAEL_TZ = timezone(timedelta(hours=3))


class Alert(BaseModel):
    event_id: str
    alert_id: str
    type: str
    severity: str
    region_name: Optional[str] = "Unknown"
    oref_city: Optional[str] = "Unknown"
    lat: Optional[float] = None
    lng: Optional[float] = None
    timestamp: datetime

    @field_validator("lat", "lng", mode="before")
    @classmethod
    def parse_coord(cls, v):
        return float(v) if v is not None else None

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v):
        if isinstance(v, datetime):
            return v
        return datetime.fromtimestamp(int(v) / 1000, tz=ISRAEL_TZ)

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "alert_id": self.alert_id,
            "type": self.type,
            "severity": self.severity,
            "region_name": self.region_name,
            "oref_city": self.oref_city,
            "lat": self.lat,
            "lng": self.lng,
            "timestamp": self.timestamp.isoformat(),
        }
