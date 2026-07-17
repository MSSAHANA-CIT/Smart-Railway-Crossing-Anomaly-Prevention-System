"""Shared validation helpers for railway organization and device management."""

from typing import Optional

from fastapi import HTTPException, status


def require_valid_choice(
    value: str,
    valid_values: tuple[str, ...],
    *,
    field_name: str,
) -> str:
    """Raise 400 if value is not in the controlled vocabulary."""
    if value not in valid_values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid {field_name} '{value}'. "
                f"Must be one of: {', '.join(valid_values)}"
            ),
        )
    return value


def require_entity(
    entity: Optional[object],
    *,
    name: str,
) -> object:
    """Raise 404 when an expected entity is missing."""
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{name} not found.",
        )
    return entity


def conflict(detail: str) -> HTTPException:
    """Return a 409 Conflict HTTPException."""
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def bad_request(detail: str) -> HTTPException:
    """Return a 400 Bad Request HTTPException."""
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
