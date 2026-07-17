"""Staff assignment API tests."""

from fastapi.testclient import TestClient

from app.models.user import User


def test_staff_assignment_requires_valid_user_and_rejects_duplicate(
    client: TestClient,
    admin_headers: dict[str, str],
    viewer_user: User,
    unique_code: str,
) -> None:
    zone = client.post(
        "/api/railway/zones",
        headers=admin_headers,
        json={"zone_code": f"TZ-SA-{unique_code}", "zone_name": "Staff Zone"},
    ).json()

    bad_user = client.post(
        "/api/staff-assignments",
        headers=admin_headers,
        json={
            "user_id": 99999999,
            "assignment_type": "ZONE",
            "zone_id": zone["id"],
        },
    )
    assert bad_user.status_code == 404

    first = client.post(
        "/api/staff-assignments",
        headers=admin_headers,
        json={
            "user_id": viewer_user.id,
            "assignment_type": "ZONE",
            "zone_id": zone["id"],
            "responsibility": "Demo oversight",
        },
    )
    assert first.status_code == 201, first.text

    duplicate = client.post(
        "/api/staff-assignments",
        headers=admin_headers,
        json={
            "user_id": viewer_user.id,
            "assignment_type": "ZONE",
            "zone_id": zone["id"],
        },
    )
    assert duplicate.status_code == 409
