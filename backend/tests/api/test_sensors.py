"""Sensor registration API tests."""

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sensor_type import SensorType


def test_sensor_requires_valid_type_and_device(
    client: TestClient,
    admin_headers: dict[str, str],
    db: Session,
    unique_code: str,
) -> None:
    device = client.post(
        "/api/devices",
        headers=admin_headers,
        json={
            "device_code": f"DEV-SN-{unique_code}",
            "device_name": "Sensor Host",
            "device_type": "ESP32_SENSOR_CONTROLLER",
            "communication_type": "SIMULATED",
        },
    ).json()

    bad_type = client.post(
        "/api/sensors",
        headers=admin_headers,
        json={
            "sensor_code": f"SN-BADT-{unique_code}",
            "sensor_name": "Bad Type",
            "sensor_type_id": 99999999,
            "device_id": device["id"],
        },
    )
    assert bad_type.status_code == 404

    bad_device = client.post(
        "/api/sensors",
        headers=admin_headers,
        json={
            "sensor_code": f"SN-BADD-{unique_code}",
            "sensor_name": "Bad Device",
            "sensor_type_id": 1,
            "device_id": 99999999,
        },
    )
    assert bad_device.status_code == 404

    sensor_type = db.scalar(select(SensorType).where(SensorType.code == "IR_ENTRY"))
    assert sensor_type is not None

    good = client.post(
        "/api/sensors",
        headers=admin_headers,
        json={
            "sensor_code": f"SN-OK-{unique_code}",
            "sensor_name": "Good Sensor",
            "sensor_type_id": sensor_type.id,
            "device_id": device["id"],
            "gpio_reference": "PROVISIONAL-GPIO-X",
        },
    )
    assert good.status_code == 201, good.text
    assert good.json()["health_status"] == "UNKNOWN"

    duplicate = client.post(
        "/api/sensors",
        headers=admin_headers,
        json={
            "sensor_code": f"SN-OK-{unique_code}",
            "sensor_name": "Dup Sensor",
            "sensor_type_id": sensor_type.id,
            "device_id": device["id"],
        },
    )
    assert duplicate.status_code == 409
