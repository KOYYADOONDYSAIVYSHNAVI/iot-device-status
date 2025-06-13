from datetime import datetime, timedelta
from validators import (
    is_valid_battery_level,
    is_valid_timestamp,
    is_online_rssi_consistent
)

def test_valid_battery_level():
    assert is_valid_battery_level(50)
    assert not is_valid_battery_level(-1)
    assert not is_valid_battery_level(150)

def test_valid_timestamp():
    assert is_valid_timestamp(datetime.utcnow())
    assert not is_valid_timestamp(datetime.utcnow() + timedelta(days=1))  # future
    assert not is_valid_timestamp(datetime.utcnow() - timedelta(days=400))  # too old

def test_online_rssi_consistency():
    assert is_online_rssi_consistent(True, -30)
    assert not is_online_rssi_consistent(False, -20)  # too strong signal to be offline
