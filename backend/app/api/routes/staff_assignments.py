"""Staff assignment routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import ROLE_RAILWAY_ADMIN, ROLE_SUPER_ADMIN, User
from app.schemas.pagination import PaginatedResponse
from app.schemas.staff_assignment import (
    StaffAssignmentCreate,
    StaffAssignmentResponse,
    StaffAssignmentUpdate,
)
from app.services.rbac import ORG_READ_ROLES, STAFF_ASSIGNMENT_WRITE_ROLES
from app.services.staff_assignment_service import (
    activate_assignment,
    create_assignment,
    deactivate_assignment,
    get_assignment_by_id,
    list_assignments,
    update_assignment,
)
from app.services.user_service import get_user_by_id
from app.utils.pagination import PaginationParams, build_paginated_response, pagination_params
from app.utils.validation import require_entity

router = APIRouter(tags=["Staff Assignments"])


@router.post(
    "/staff-assignments",
    response_model=StaffAssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create staff assignment",
)
def create_assignment_endpoint(
    body: StaffAssignmentCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(STAFF_ASSIGNMENT_WRITE_ROLES))],
) -> StaffAssignmentResponse:
    """
    Assign a user to a zone, division, station, crossing, or device.

    Prevents exact active duplicate assignments.
    """
    assignment = create_assignment(
        db, body, actor=current_user.email, actor_user_id=current_user.id
    )
    return StaffAssignmentResponse.model_validate(assignment)


@router.get(
    "/staff-assignments",
    response_model=PaginatedResponse[StaffAssignmentResponse],
    summary="List staff assignments",
)
def list_assignments_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    user_id: Optional[int] = None,
    assignment_type: Optional[str] = None,
    zone_id: Optional[int] = None,
    division_id: Optional[int] = None,
    station_id: Optional[int] = None,
    crossing_id: Optional[int] = None,
    device_id: Optional[int] = None,
    is_active: Optional[bool] = None,
) -> PaginatedResponse[StaffAssignmentResponse]:
    items, total = list_assignments(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        user_id=user_id,
        assignment_type=assignment_type,
        zone_id=zone_id,
        division_id=division_id,
        station_id=station_id,
        crossing_id=crossing_id,
        device_id=device_id,
        is_active=is_active,
    )
    return build_paginated_response(
        [StaffAssignmentResponse.model_validate(a) for a in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get(
    "/staff-assignments/{assignment_id}",
    response_model=StaffAssignmentResponse,
    summary="Get staff assignment",
)
def get_assignment_endpoint(
    assignment_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
) -> StaffAssignmentResponse:
    assignment = require_entity(
        get_assignment_by_id(db, assignment_id), name="Staff assignment"
    )
    return StaffAssignmentResponse.model_validate(assignment)


@router.patch(
    "/staff-assignments/{assignment_id}",
    response_model=StaffAssignmentResponse,
    summary="Update staff assignment",
)
def update_assignment_endpoint(
    assignment_id: int,
    body: StaffAssignmentUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(STAFF_ASSIGNMENT_WRITE_ROLES))],
) -> StaffAssignmentResponse:
    assignment = update_assignment(
        db, assignment_id, body, actor=current_user.email
    )
    return StaffAssignmentResponse.model_validate(assignment)


@router.patch(
    "/staff-assignments/{assignment_id}/activate",
    response_model=StaffAssignmentResponse,
    summary="Activate staff assignment",
)
def activate_assignment_endpoint(
    assignment_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(STAFF_ASSIGNMENT_WRITE_ROLES))],
) -> StaffAssignmentResponse:
    assignment = activate_assignment(db, assignment_id, actor=current_user.email)
    return StaffAssignmentResponse.model_validate(assignment)


@router.patch(
    "/staff-assignments/{assignment_id}/deactivate",
    response_model=StaffAssignmentResponse,
    summary="Deactivate staff assignment",
)
def deactivate_assignment_endpoint(
    assignment_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(STAFF_ASSIGNMENT_WRITE_ROLES))],
) -> StaffAssignmentResponse:
    assignment = deactivate_assignment(db, assignment_id, actor=current_user.email)
    return StaffAssignmentResponse.model_validate(assignment)


@router.get(
    "/users/{user_id}/assignments",
    response_model=PaginatedResponse[StaffAssignmentResponse],
    summary="List assignments for a user",
    tags=["Staff Assignments"],
)
def list_user_assignments_endpoint(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    is_active: Optional[bool] = None,
) -> PaginatedResponse[StaffAssignmentResponse]:
    """
    List assignments for a user.

    Allowed for SUPER_ADMIN, RAILWAY_ADMIN, or the user viewing their own assignments.
    """
    admin_roles = {ROLE_SUPER_ADMIN, ROLE_RAILWAY_ADMIN}
    if current_user.role not in admin_roles and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view these assignments.",
        )

    require_entity(get_user_by_id(db, user_id), name="User")
    items, total = list_assignments(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        user_id=user_id,
        is_active=is_active,
    )
    return build_paginated_response(
        [StaffAssignmentResponse.model_validate(a) for a in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )
