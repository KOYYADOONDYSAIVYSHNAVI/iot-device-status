import datetime
from fastapi.testclient import TestClient
from main import app
from routers.status import get_db  
from routers.test_database import override_get_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_post_and_get_device_status():
    payload = {
        "device_id": "sensor-integration-1234567",
        "timestamp": datetime.datetime.now().isoformat(),
        "battery_level": 85,
        "rssi": -70,
        "online": True
    }

    response = client.post("/status/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Payload stored successfully."}

    get_response = client.get(f"/status/{payload['device_id']}")
    assert get_response.status_code == 200
    data = get_response.json()

    assert data["device_id"] == payload["device_id"]
    assert data["battery_level"] == payload["battery_level"]
    assert data["rssi"] == payload["rssi"]
    assert data["online"] == payload["online"]

def test_get_status_summary():
    devices = [
        {
            "device_id": "sensor-summary-1",
            "timestamp": datetime.datetime.now().isoformat(),
            "battery_level": 90,
            "rssi": -50,
            "online": True
        },
        {
            "device_id": "sensor-summary-2",
            "timestamp": datetime.datetime.now().isoformat(),
            "battery_level": 70,
            "rssi": -80,
            "online": False
        }
    ]

    for device in devices:
        response = client.post("/status/", json=device)
        assert response.status_code == 200

    summary_response = client.get("/status/summary")
    assert summary_response.status_code == 200
    summary_data = summary_response.json()

    device_ids_in_summary = [d["device_id"] for d in summary_data]
    for device in devices:
        assert device["device_id"] in device_ids_in_summary

    for device_summary in summary_data:
        assert "device_id" in device_summary
        assert "battery_level" in device_summary
        assert "online" in device_summary
        assert "last_updated" in device_summary
