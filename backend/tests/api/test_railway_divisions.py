"""Railway division and station hierarchy tests."""

from fastapi.testclient import TestClient


def _create_zone(client: TestClient, headers: dict[str, str], code: str) -> int:
    response = client.post(
        "/api/railway/zones",
        headers=headers,
        json={"zone_code": code, "zone_name": f"Zone {code}"},
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_division_invalid_zone(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    response = client.post(
        "/api/railway/divisions",
        headers=admin_headers,
        json={
            "division_code": f"TD-{unique_code}",
            "division_name": "Bad Zone Division",
            "zone_id": 99999999,
        },
    )
    assert response.status_code == 404


def test_division_valid_zone(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    zone_id = _create_zone(client, admin_headers, f"TZ-D-{unique_code}")
    response = client.post(
        "/api/railway/divisions",
        headers=admin_headers,
        json={
            "division_code": f"TD-{unique_code}",
            "division_name": "Valid Division",
            "zone_id": zone_id,
        },
    )
    assert response.status_code == 201, response.text
    assert response.json()["zone_id"] == zone_id


def test_station_invalid_division(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    response = client.post(
        "/api/railway/stations",
        headers=admin_headers,
        json={
            "station_code": f"TS-{unique_code}",
            "station_name": "Bad Division Station",
            "division_id": 99999999,
        },
    )
    assert response.status_code == 404
