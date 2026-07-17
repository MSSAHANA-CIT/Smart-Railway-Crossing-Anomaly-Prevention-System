"""Railway crossing hierarchy validation tests."""

from fastapi.testclient import TestClient


def _hierarchy(
    client: TestClient, headers: dict[str, str], unique_code: str
) -> dict[str, int]:
    zone = client.post(
        "/api/railway/zones",
        headers=headers,
        json={"zone_code": f"TZ-C-{unique_code}", "zone_name": "Crossing Zone"},
    ).json()
    division = client.post(
        "/api/railway/divisions",
        headers=headers,
        json={
            "division_code": f"TD-C-{unique_code}",
            "division_name": "Crossing Division",
            "zone_id": zone["id"],
        },
    ).json()
    station = client.post(
        "/api/railway/stations",
        headers=headers,
        json={
            "station_code": f"TS-C-{unique_code}",
            "station_name": "Crossing Station",
            "division_id": division["id"],
        },
    ).json()
    return {
        "zone_id": zone["id"],
        "division_id": division["id"],
        "station_id": station["id"],
    }


def test_crossing_hierarchy_must_be_consistent(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    h = _hierarchy(client, admin_headers, unique_code)
    other_zone = client.post(
        "/api/railway/zones",
        headers=admin_headers,
        json={"zone_code": f"TZ-C2-{unique_code}", "zone_name": "Other Zone"},
    ).json()

    bad = client.post(
        "/api/railway/crossings",
        headers=admin_headers,
        json={
            "crossing_code": f"TC-BAD-{unique_code}",
            "crossing_name": "Bad Hierarchy Crossing",
            "station_id": h["station_id"],
            "division_id": h["division_id"],
            "zone_id": other_zone["id"],
        },
    )
    assert bad.status_code == 400

    good = client.post(
        "/api/railway/crossings",
        headers=admin_headers,
        json={
            "crossing_code": f"TC-OK-{unique_code}",
            "crossing_name": "Good Hierarchy Crossing",
            "station_id": h["station_id"],
            "division_id": h["division_id"],
            "zone_id": h["zone_id"],
            "crossing_type": "MANNED",
            "gate_type": "PROTOTYPE",
        },
    )
    assert good.status_code == 201, good.text
