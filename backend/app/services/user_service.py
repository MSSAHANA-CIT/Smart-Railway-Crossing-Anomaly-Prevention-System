"""User management service."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import (
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    VALID_ROLES,
    User,
)
from app.schemas.user import UserCreate
from app.services.audit_service import USER_CREATED, USER_DISABLED, USER_ENABLED, create_audit_log


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Return a user by email address, or None."""
    return db.scalar(select(User).where(User.email == email))


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Return a user by primary key, or None."""
    return db.get(User, user_id)


def list_users(db: Session, *, skip: int = 0, limit: int = 100) -> list[User]:
    """Return a paginated list of users ordered by creation date."""
    return list(
        db.scalars(
            select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
        )
    )


def count_users(db: Session) -> int:
    """Return total number of users in the database."""
    return db.scalar(select(func.count()).select_from(User)) or 0


def create_user(
    db: Session,
    user_in: UserCreate,
    *,
    actor: str = "system",
) -> User:
    """Create a new user with hashed password."""
    if user_in.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}",
        )

    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    create_audit_log(
        db,
        actor=actor,
        action=USER_CREATED,
        entity_type="user",
        entity_id=str(user.id),
        details=f"User created: {user.email} role={user.role}",
    )
    return user


def disable_user(db: Session, user_id: int, *, actor: str) -> User:
    """Disable a user account."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    user.is_active = False
    user.status = STATUS_INACTIVE
    db.commit()
    db.refresh(user)

    create_audit_log(
        db,
        actor=actor,
        action=USER_DISABLED,
        entity_type="user",
        entity_id=str(user.id),
        details=f"User disabled: {user.email}",
    )
    return user


def enable_user(db: Session, user_id: int, *, actor: str) -> User:
    """Enable a previously disabled user account."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    user.is_active = True
    user.status = STATUS_ACTIVE
    db.commit()
    db.refresh(user)

    create_audit_log(
        db,
        actor=actor,
        action=USER_ENABLED,
        entity_type="user",
        entity_id=str(user.id),
        details=f"User enabled: {user.email}",
    )
    return user
