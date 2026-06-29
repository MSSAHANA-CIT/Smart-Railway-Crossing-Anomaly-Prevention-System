"""FastAPI dependencies for authentication and role-based access control."""

from typing import Annotated, Callable, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import get_current_user_from_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)
    ],
) -> User:
    """Extract JWT from Authorization header and return the authenticated user."""
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_current_user_from_token(db, credentials.credentials)
    return user


def get_current_user_optional(
    db: Annotated[Session, Depends(get_db)],
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)
    ],
) -> Optional[User]:
    """Return authenticated user or None when no bearer token is provided."""
    if credentials is None or not credentials.credentials:
        return None
    try:
        return get_current_user_from_token(db, credentials.credentials)
    except HTTPException:
        return None


def require_roles(allowed_roles: list[str]) -> Callable:
    """Return a dependency that enforces role-based access."""

    def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this action.",
            )
        return current_user

    return role_checker
