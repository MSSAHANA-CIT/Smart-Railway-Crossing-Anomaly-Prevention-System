"""User management routes with role-based access control."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_current_user_optional, require_roles
from app.db.session import get_db
from app.models.user import ROLE_RAILWAY_ADMIN, ROLE_SUPER_ADMIN, User
from app.schemas.user import CurrentUserResponse, UserCreate, UserResponse
from app.services.audit_service import USER_PROFILE_VIEWED, create_audit_log
from app.services.user_service import (
    count_users,
    create_user,
    disable_user,
    enable_user,
    get_user_by_id,
    list_users,
)

router = APIRouter(prefix="/users", tags=["Users"])

ADMIN_ROLES = [ROLE_SUPER_ADMIN, ROLE_RAILWAY_ADMIN]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    body: UserCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Optional[User], Depends(get_current_user_optional)] = None,
) -> UserResponse:
    """
    Create a new user.

    Allowed without authentication only when no users exist (bootstrap).
    Otherwise requires SUPER_ADMIN role.
    """
    user_count = count_users(db)

    if user_count > 0:
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required to create users.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if current_user.role != ROLE_SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only SUPER_ADMIN can create users.",
            )
        actor = current_user.email
    else:
        actor = "bootstrap"

    user = create_user(db, body, actor=actor)
    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
def list_users_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ADMIN_ROLES))],
    skip: int = 0,
    limit: int = 100,
) -> list[UserResponse]:
    """List users. Requires SUPER_ADMIN or RAILWAY_ADMIN."""
    users = list_users(db, skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """
    Get user by ID.

    Allowed for SUPER_ADMIN, RAILWAY_ADMIN, or the user viewing their own profile.
    """
    if current_user.role not in ADMIN_ROLES and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view this user.",
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    create_audit_log(
        db,
        actor=current_user.email,
        action=USER_PROFILE_VIEWED,
        entity_type="user",
        entity_id=str(user.id),
        details=f"Profile viewed: {user.email}",
    )
    return UserResponse.model_validate(user)


@router.patch("/{user_id}/disable", response_model=UserResponse)
def disable_user_endpoint(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(ADMIN_ROLES))],
) -> UserResponse:
    """Disable a user account. Requires SUPER_ADMIN or RAILWAY_ADMIN."""
    user = disable_user(db, user_id, actor=current_user.email)
    return UserResponse.model_validate(user)


@router.patch("/{user_id}/enable", response_model=UserResponse)
def enable_user_endpoint(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(ADMIN_ROLES))],
) -> UserResponse:
    """Enable a user account. Requires SUPER_ADMIN or RAILWAY_ADMIN."""
    user = enable_user(db, user_id, actor=current_user.email)
    return UserResponse.model_validate(user)
