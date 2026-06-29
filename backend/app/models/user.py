"""User model with IAM fields for authentication and role-based access."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

# Role values (string field — no separate roles table in Phase S3)
ROLE_SUPER_ADMIN = "SUPER_ADMIN"
ROLE_RAILWAY_ADMIN = "RAILWAY_ADMIN"
ROLE_DIVISION_ADMIN = "DIVISION_ADMIN"
ROLE_STATION_MASTER = "STATION_MASTER"
ROLE_CROSSING_OPERATOR = "CROSSING_OPERATOR"
ROLE_MAINTENANCE_ENGINEER = "MAINTENANCE_ENGINEER"
ROLE_SAFETY_INSPECTOR = "SAFETY_INSPECTOR"
ROLE_VIEWER = "VIEWER"

VALID_ROLES = (
    ROLE_SUPER_ADMIN,
    ROLE_RAILWAY_ADMIN,
    ROLE_DIVISION_ADMIN,
    ROLE_STATION_MASTER,
    ROLE_CROSSING_OPERATOR,
    ROLE_MAINTENANCE_ENGINEER,
    ROLE_SAFETY_INSPECTOR,
    ROLE_VIEWER,
)

# Status values
STATUS_ACTIVE = "ACTIVE"
STATUS_INACTIVE = "INACTIVE"
STATUS_SUSPENDED = "SUSPENDED"
STATUS_PENDING = "PENDING"

VALID_STATUSES = (
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    STATUS_SUSPENDED,
    STATUS_PENDING,
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ROLE_VIEWER
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STATUS_ACTIVE
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
