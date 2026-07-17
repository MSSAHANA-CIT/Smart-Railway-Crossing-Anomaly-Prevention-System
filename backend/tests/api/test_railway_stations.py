"""Railway station API tests."""

from fastapi.testclient import TestClient


def _setup_division(
    client: TestClient, headers: dict[str, str], unique_code: str
) -> tuple[int, int]:
    zone = client.post(
        "/api/railway/zones",
        headers=headers,
        json={"zone_code": f"TZ-S-{unique_code}", "zone_name": "Station Zone"},
    ).json()
    division = client.post(
        "/api/railway/divisions",
        headers=headers,
        json={
            "division_code": f"TD-S-{unique_code}",
            "division_name": "Station Division",
            "zone_id": zone["id"],
        },
    ).json()
    return zone["id"], division["id"]


def test_create_station(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    _, division_id = _setup_division(client, admin_headers, unique_code)
    response = client.post(
        "/api/railway/stations",
        headers=admin_headers,
        json={
            "station_code": f"TS-{unique_code}",
            "station_name": "Test Station",
            "division_id": division_id,
            "station_type": "STANDARD",
        },
    )
    assert response.status_code == 201, response.text
    assert response.json()["division_id"] == division_id
