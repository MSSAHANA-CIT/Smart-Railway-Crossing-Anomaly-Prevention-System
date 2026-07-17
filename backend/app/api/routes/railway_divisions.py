"""Railway division management routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.pagination import PaginatedResponse
from app.schemas.railway_division import (
    RailwayDivisionCreate,
    RailwayDivisionResponse,
    RailwayDivisionUpdate,
)
from app.services.rbac import DIVISION_WRITE_ROLES, ORG_READ_ROLES
from app.services.railway_division_service import (
    activate_division,
    create_division,
    deactivate_division,
    get_division_by_id,
    list_divisions,
    update_division,
)
from app.utils.pagination import PaginationParams, build_paginated_response, pagination_params
from app.utils.validation import require_entity

router = APIRouter(prefix="/railway/divisions", tags=["Railway Divisions"])


@router.post(
    "",
    response_model=RailwayDivisionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create railway division",
)
def create_division_endpoint(
    body: RailwayDivisionCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DIVISION_WRITE_ROLES))],
) -> RailwayDivisionResponse:
    """Create a division under a zone. Validates parent zone existence."""
    division = create_division(
        db, body, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayDivisionResponse.model_validate(division)


@router.get(
    "",
    response_model=PaginatedResponse[RailwayDivisionResponse],
    summary="List railway divisions",
)
def list_divisions_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    zone_id: Optional[int] = None,
    status_filter: Annotated[Optional[str], Query(alias="status")] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> PaginatedResponse[RailwayDivisionResponse]:
    items, total = list_divisions(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        zone_id=zone_id,
        status=status_filter,
        is_active=is_active,
        search=search,
    )
    return build_paginated_response(
        [RailwayDivisionResponse.model_validate(d) for d in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get(
    "/{division_id}",
    response_model=RailwayDivisionResponse,
    summary="Get division details",
)
def get_division_endpoint(
    division_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
) -> RailwayDivisionResponse:
    division = require_entity(
        get_division_by_id(db, division_id), name="Railway division"
    )
    return RailwayDivisionResponse.model_validate(division)


@router.patch(
    "/{division_id}",
    response_model=RailwayDivisionResponse,
    summary="Update division",
)
def update_division_endpoint(
    division_id: int,
    body: RailwayDivisionUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DIVISION_WRITE_ROLES))],
) -> RailwayDivisionResponse:
    division = update_division(
        db,
        division_id,
        body,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return RailwayDivisionResponse.model_validate(division)


@router.patch(
    "/{division_id}/activate",
    response_model=RailwayDivisionResponse,
    summary="Activate division",
)
def activate_division_endpoint(
    division_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DIVISION_WRITE_ROLES))],
) -> RailwayDivisionResponse:
    division = activate_division(
        db, division_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayDivisionResponse.model_validate(division)


@router.patch(
    "/{division_id}/deactivate",
    response_model=RailwayDivisionResponse,
    summary="Deactivate division",
)
def deactivate_division_endpoint(
    division_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DIVISION_WRITE_ROLES))],
) -> RailwayDivisionResponse:
    division = deactivate_division(
        db, division_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayDivisionResponse.model_validate(division)
