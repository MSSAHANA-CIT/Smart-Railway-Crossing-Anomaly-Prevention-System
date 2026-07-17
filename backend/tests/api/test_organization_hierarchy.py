"""Organization hierarchy and auth continuity tests."""

from fastapi.testclient import TestClient

from app.models.user import User


def test_organization_hierarchy_parent_child(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    zone = client.post(
        "/api/railway/zones",
        headers=admin_headers,
        json={"zone_code": f"TZ-H-{unique_code}", "zone_name": "Hierarchy Zone"},
    ).json()
    division = client.post(
        "/api/railway/divisions",
        headers=admin_headers,
        json={
            "division_code": f"TD-H-{unique_code}",
            "division_name": "Hierarchy Division",
            "zone_id": zone["id"],
        },
    ).json()
    station = client.post(
        "/api/railway/stations",
        headers=admin_headers,
        json={
            "station_code": f"TS-H-{unique_code}",
            "station_name": "Hierarchy Station",
            "division_id": division["id"],
        },
    ).json()
    crossing = client.post(
        "/api/railway/crossings",
        headers=admin_headers,
        json={
            "crossing_code": f"TC-H-{unique_code}",
            "crossing_name": "Hierarchy Crossing",
            "station_id": station["id"],
            "division_id": division["id"],
            "zone_id": zone["id"],
        },
    ).json()

    hierarchy = client.get(
        "/api/railway/hierarchy",
        headers=admin_headers,
        params={"zone_id": zone["id"]},
    )
    assert hierarchy.status_code == 200, hierarchy.text
    body = hierarchy.json()
    assert len(body["zones"]) == 1
    assert body["zones"][0]["zone_code"] == zone["zone_code"]
    assert body["zones"][0]["divisions"][0]["division_code"] == division["division_code"]
    assert (
        body["zones"][0]["divisions"][0]["stations"][0]["station_code"]
        == station["station_code"]
    )
    assert (
        body["zones"][0]["divisions"][0]["stations"][0]["crossings"][0]["crossing_code"]
        == crossing["crossing_code"]
    )

    overview = client.get(
        f"/api/railway/crossings/{crossing['id']}/overview",
        headers=admin_headers,
    )
    assert overview.status_code == 200
    assert overview.json()["zone"]["id"] == zone["id"]
    assert overview.json()["station"]["id"] == station["id"]


def test_existing_auth_endpoints_still_work(
    client: TestClient, super_admin: User, admin_headers: dict[str, str]
) -> None:
    me = client.get("/api/auth/me", headers=admin_headers)
    assert me.status_code == 200
    assert me.json()["email"] == super_admin.email

    verify = client.post(
        "/api/auth/verify-token",
        headers=admin_headers,
    )
    assert verify.status_code == 200

    health = client.get("/api/health")
    assert health.status_code == 200

    root = client.get("/")
    assert root.status_code == 200
