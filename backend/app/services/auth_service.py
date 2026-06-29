"""Authentication service — login, credential validation, and token resolution."""

from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, decode_access_token, verify_password
from app.models.user import STATUS_ACTIVE, User
from app.schemas.auth import TokenResponse
from app.schemas.user import CurrentUserResponse
from app.services.audit_service import (
    USER_LOGIN_FAILED,
    USER_LOGIN_SUCCESS,
    create_audit_log,
)
from app.services.user_service import get_user_by_email, get_user_by_id

settings = get_settings()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Validate credentials. Returns user on success, None on failure."""
    user = get_user_by_email(db, email)
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        user.failed_login_attempts += 1
        db.commit()
        create_audit_log(
            db,
            actor=email,
            action=USER_LOGIN_FAILED,
            entity_type="user",
            entity_id=str(user.id) if user else None,
            details="Invalid password",
        )
        return None

    if not user.is_active or user.status != STATUS_ACTIVE:
        create_audit_log(
            db,
            actor=email,
            action=USER_LOGIN_FAILED,
            entity_type="user",
            entity_id=str(user.id),
            details=f"Account not active: status={user.status}",
        )
        return None

    return user


def login_user(db: Session, email: str, password: str) -> TokenResponse:
    """Authenticate user and return JWT access token with user profile."""
    user = get_user_by_email(db, email)

    if not user:
        create_audit_log(
            db,
            actor=email,
            action=USER_LOGIN_FAILED,
            entity_type="user",
            details="Unknown email",
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    authenticated = authenticate_user(db, email, password)
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    user = authenticated
    user.last_login_at = datetime.now(timezone.utc)
    user.failed_login_attempts = 0
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        subject=user.email,
        user_id=user.id,
        role=user.role,
    )

    create_audit_log(
        db,
        actor=user.email,
        action=USER_LOGIN_SUCCESS,
        entity_type="user",
        entity_id=str(user.id),
        details="Login successful",
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=CurrentUserResponse.model_validate(user),
    )


def get_current_user_from_token(db: Session, token: str) -> User:
    """Resolve and return the user from a JWT access token."""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active or user.status != STATUS_ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled.",
        )

    return user
