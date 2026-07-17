"""Railway zone API tests."""

from fastapi.testclient import TestClient


def test_zones_require_auth(client: TestClient) -> None:
    response = client.get("/api/railway/zones")
    assert response.status_code == 401


def test_viewer_cannot_create_zone(
    client: TestClient, viewer_headers: dict[str, str], unique_code: str
) -> None:
    response = client.post(
        "/api/railway/zones",
        headers=viewer_headers,
        json={
            "zone_code": f"TZ-{unique_code}",
            "zone_name": "Viewer Denied Zone",
        },
    )
    assert response.status_code == 403


def test_super_admin_can_create_zone(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    code = f"TZ-{unique_code}"
    response = client.post(
        "/api/railway/zones",
        headers=admin_headers,
        json={"zone_code": code, "zone_name": "Test Zone"},
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["zone_code"] == code
    assert body["is_active"] is True


def test_duplicate_zone_code_conflict(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    code = f"TZ-DUP-{unique_code}"
    payload = {"zone_code": code, "zone_name": "Dup Zone"}
    first = client.post("/api/railway/zones", headers=admin_headers, json=payload)
    assert first.status_code == 201
    second = client.post("/api/railway/zones", headers=admin_headers, json=payload)
    assert second.status_code == 409


def test_zone_pagination_and_search(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    code = f"TZ-SRCH-{unique_code}"
    client.post(
        "/api/railway/zones",
        headers=admin_headers,
        json={"zone_code": code, "zone_name": f"Searchable Zone {unique_code}"},
    )
    response = client.get(
        "/api/railway/zones",
        headers=admin_headers,
        params={"search": unique_code, "page": 1, "page_size": 10},
    )
    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "total" in body
    assert body["page"] == 1
    assert any(item["zone_code"] == code for item in body["items"])


def test_zone_deactivate_preserves_record(
    client: TestClient, admin_headers: dict[str, str], unique_code: str
) -> None:
    create = client.post(
        "/api/railway/zones",
        headers=admin_headers,
        json={"zone_code": f"TZ-OFF-{unique_code}", "zone_name": "Deactivate Me"},
    )
    zone_id = create.json()["id"]
    deactivate = client.patch(
        f"/api/railway/zones/{zone_id}/deactivate", headers=admin_headers
    )
    assert deactivate.status_code == 200
    assert deactivate.json()["is_active"] is False
    fetch = client.get(f"/api/railway/zones/{zone_id}", headers=admin_headers)
    assert fetch.status_code == 200
    assert fetch.json()["id"] == zone_id
