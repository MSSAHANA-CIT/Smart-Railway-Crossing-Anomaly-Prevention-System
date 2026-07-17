"""Device management API tests."""

from fastapi.testclient import TestClient


def _create_crossing(
    client: TestClient, headers: dict[str, str], unique_code: str
) -> int:
    zone = client.post(
        "/api/railway/zones",
        headers=headers,
        json={"zone_code": f"TZ-DV-{unique_code}", "zone_name": "Device Zone"},
    ).json()
    division = client.post(
        "/api/railway/divisions",
        headers=headers,
        json={
            "division_code": f"TD-DV-{unique_code}",
            "division_name": "Device Division",
            "zone_id": zone["id"],
        },
    ).json()
    station = client.post(
        "/api/railway/stations",
        headers=headers,
        json={
            "station_code": f"TS-DV-{unique_code}",
            "station_name": "Device Station",
            "division_id": division["id"],
        },
    ).json()
    crossing = client.post(
        "/api/railway/crossings",
        headers=headers,
        json={
            "crossing_code": f"TC-DV-{unique_code}",
            "crossing_name": "Device Crossing",
            "station_id": station["id"],
            "division_id": division["id"],
            "zone_id": zone["id"],
        },
    ).json()
    return crossing["id"]


def test_device_register_without_crossing(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    response = client.post(
        "/api/devices",
        headers=admin_headers,
        json={
            "device_code": f"DEV-{unique_code}",
            "device_name": "Unassigned Controller",
            "device_type": "ESP32_SENSOR_CONTROLLER",
            "communication_type": "SIMULATED",
        },
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["crossing_id"] is None
    assert body["health_status"] == "UNKNOWN"
    assert body["status"] == "REGISTERED"


def test_device_assign_and_reject_second_crossing(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    crossing_a = _create_crossing(client, admin_headers, f"A{unique_code}")
    crossing_b = _create_crossing(client, admin_headers, f"B{unique_code}")

    device = client.post(
        "/api/devices",
        headers=admin_headers,
        json={
            "device_code": f"DEV-ASG-{unique_code}",
            "device_name": "Assignable Device",
            "device_type": "ESP32S3_AI_CAMERA",
            "communication_type": "SIMULATED",
        },
    ).json()

    assign_a = client.post(
        f"/api/devices/{device['id']}/assign",
        headers=admin_headers,
        json={"crossing_id": crossing_a},
    )
    assert assign_a.status_code == 200
    assert assign_a.json()["crossing_id"] == crossing_a

    assign_b = client.post(
        f"/api/devices/{device['id']}/assign",
        headers=admin_headers,
        json={"crossing_id": crossing_b},
    )
    assert assign_b.status_code == 409
