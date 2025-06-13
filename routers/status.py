from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List
import os
from database import SessionLocal, engine
from models import DeviceStatus as DeviceStatusModel

router = APIRouter()

DeviceStatusModel.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DeviceStatus(BaseModel):
    device_id: str
    timestamp: datetime
    battery_level: int = Field(..., ge=0, le=100, description="Battery level must be between 0 and 100")
    rssi: int
    online: bool
    @field_validator('timestamp')
    def timestamp_not_in_future(cls, v):
        if v.tzinfo is not None:
            v = v.replace(tzinfo=None)
        if v > datetime.utcnow():
            raise ValueError("Timestamp cannot be in the future")
        return v

API_KEY = os.getenv("API_KEY") 
API_KEY_NAME = "IOT-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

router = APIRouter()


@router.post("/" , dependencies=[Depends(get_api_key)])
def store_payload(payload: DeviceStatus, db: Session = Depends(get_db)):
    db_status = DeviceStatusModel(
        device_id=payload.device_id,
        timestamp=payload.timestamp,
        battery_level=payload.battery_level,
        rssi=payload.rssi,
        online=payload.online
    )
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return {"message": "Payload stored successfully."}

@router.get("/summary", dependencies=[Depends(get_api_key)])
def get_device_summary(db: Session = Depends(get_db)):
    all_records = db.query(DeviceStatusModel).all()
    for record in all_records:
        print(f"  - {record.device_id}, {record.timestamp}, {record.battery_level}, {record.online}")

    subquery = (
        db.query(
            DeviceStatusModel.device_id,
            func.max(DeviceStatusModel.timestamp).label("latest_timestamp")
        )
        .group_by(DeviceStatusModel.device_id)
        .subquery()
    )

    subquery_results = db.query(subquery).all()

    latest_devices = (
        db.query(DeviceStatusModel)
        .join(
            subquery,
            (DeviceStatusModel.device_id == subquery.c.device_id) &
            (DeviceStatusModel.timestamp == subquery.c.latest_timestamp)
        )
        .all()
    )
    return [
        {
            "device_id": device.device_id,
            "battery_level": device.battery_level,
            "online": device.online,
            "last_updated": device.timestamp.isoformat()
        }
        for device in latest_devices
    ]


@router.get("/{device_id}", response_model=DeviceStatus, dependencies=[Depends(get_api_key)])
def get_device_status(device_id: str, db: Session = Depends(get_db)):
    records = db.query(DeviceStatusModel).filter(DeviceStatusModel.device_id == device_id).all()
    if not records:
        raise HTTPException(status_code=404, detail="Device not found")
    latest = max(records, key=lambda r: r.timestamp)
    return latest

@router.get("/multiple/{device_id}", dependencies=[Depends(get_api_key)]) #Tracks historical status updates per device (instead of just the last one)
def get_device_history(device_id: str, db: Session = Depends(get_db)):
    records = db.query(DeviceStatusModel).filter(DeviceStatusModel.device_id == device_id).order_by(DeviceStatusModel.timestamp).all()
    if not records:
        raise HTTPException(status_code=404, detail="Device not found")

    return {
        "device_id": device_id,
        "history": [
            {
                "timestamp": record.timestamp.isoformat(),
                "battery_level": record.battery_level,
                "rssi": record.rssi,
                "online": record.online
            }
            for record in records
        ]
    }