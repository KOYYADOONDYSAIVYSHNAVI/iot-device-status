from datetime import datetime, timedelta

def is_valid_battery_level(battery_level: int) -> bool:
    return 0 <= battery_level <= 100

def is_valid_timestamp(timestamp: datetime) -> bool:
    now = datetime.utcnow()
    return now - timedelta(days=365) <= timestamp <= now

def is_online_rssi_consistent(online: bool, rssi: int) -> bool:
    if not online and rssi > -50:
        return False
    return True
