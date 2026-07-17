"""Pytest fixtures for Phase S4 API tests against the development database."""

from __future__ import annotations

import uuid
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.seed import seed_sensor_types
from app.db.session import SessionLocal
from app.main import app
from app.models.user import (
    ROLE_SUPER_ADMIN,
    ROLE_VIEWER,
    STATUS_ACTIVE,
    User,
)


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session", autouse=True)
def ensure_sensor_types() -> None:
    seed_sensor_types()


def _unique_email(prefix: str) -> str:
    return f"{prefix}.{uuid.uuid4().hex[:10]}@s4test.localdomain.com"


def _create_user(db: Session, *, role: str, prefix: str) -> User:
    user = User(
        email=_unique_email(prefix),
        full_name=f"Test {prefix}",
        password_hash=get_password_hash("TestPass123!"),
        role=role,
        status=STATUS_ACTIVE,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture()
def super_admin(db: Session) -> User:
    return _create_user(db, role=ROLE_SUPER_ADMIN, prefix="s4-admin")


@pytest.fixture()
def viewer_user(db: Session) -> User:
    return _create_user(db, role=ROLE_VIEWER, prefix="s4-viewer")


@pytest.fixture()
def admin_headers(client: TestClient, super_admin: User) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"email": super_admin.email, "password": "TestPass123!"},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def viewer_headers(client: TestClient, viewer_user: User) -> dict[str, str]:
    response = client.post(
        "/api/auth/login",
        json={"email": viewer_user.email, "password": "TestPass123!"},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def unique_code() -> str:
    return uuid.uuid4().hex[:8].upper()
