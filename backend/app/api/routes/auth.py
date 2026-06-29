"""Authentication routes — login, current user, and token verification."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import CurrentUserResponse
from app.services.audit_service import TOKEN_VALIDATED, create_audit_log
from app.services.auth_service import login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(
    body: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    """Authenticate with email and password; returns JWT access token."""
    return login_user(db, body.email, body.password)


@router.get("/me", response_model=CurrentUserResponse)
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> CurrentUserResponse:
    """Return the currently authenticated user profile."""
    return CurrentUserResponse.model_validate(current_user)


@router.post("/verify-token")
def verify_token(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    """Validate the bearer token and return user information."""
    create_audit_log(
        db,
        actor=current_user.email,
        action=TOKEN_VALIDATED,
        entity_type="user",
        entity_id=str(current_user.id),
        details="Token verified via /api/auth/verify-token",
    )
    return {
        "valid": True,
        "user": CurrentUserResponse.model_validate(current_user),
    }
