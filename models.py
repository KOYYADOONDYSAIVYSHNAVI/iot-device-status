from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class DeviceStatus(Base):
    __tablename__ = "device_statuses"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    battery_level = Column(Integer)
    rssi = Column(Integer)
    online = Column(Boolean)
