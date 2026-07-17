"""Railway crossing management routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.pagination import PaginatedResponse
from app.schemas.railway_crossing import (
    MonitoringStatusUpdate,
    OperationalStatusUpdate,
    RailwayCrossingCreate,
    RailwayCrossingResponse,
    RailwayCrossingUpdate,
)
from app.services.rbac import (
    CROSSING_STATUS_WRITE_ROLES,
    CROSSING_WRITE_ROLES,
    ORG_READ_ROLES,
)
from app.services.railway_crossing_service import (
    activate_crossing,
    create_crossing,
    deactivate_crossing,
    get_crossing_by_id,
    list_crossings,
    update_crossing,
    update_monitoring_status,
    update_operational_status,
)
from app.utils.pagination import PaginationParams, build_paginated_response, pagination_params
from app.utils.validation import require_entity

router = APIRouter(prefix="/railway/crossings", tags=["Railway Crossings"])


@router.post(
    "",
    response_model=RailwayCrossingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create railway crossing",
)
def create_crossing_endpoint(
    body: RailwayCrossingCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(CROSSING_WRITE_ROLES))],
) -> RailwayCrossingResponse:
    """Create a crossing. Validates station → division → zone hierarchy."""
    crossing = create_crossing(
        db, body, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayCrossingResponse.model_validate(crossing)


@router.get(
    "",
    response_model=PaginatedResponse[RailwayCrossingResponse],
    summary="List railway crossings",
)
def list_crossings_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    zone_id: Optional[int] = None,
    division_id: Optional[int] = None,
    station_id: Optional[int] = None,
    crossing_type: Optional[str] = None,
    operational_status: Optional[str] = None,
    monitoring_status: Optional[str] = None,
    risk_category: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> PaginatedResponse[RailwayCrossingResponse]:
    items, total = list_crossings(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        zone_id=zone_id,
        division_id=division_id,
        station_id=station_id,
        crossing_type=crossing_type,
        operational_status=operational_status,
        monitoring_status=monitoring_status,
        risk_category=risk_category,
        is_active=is_active,
        search=search,
    )
    return build_paginated_response(
        [RailwayCrossingResponse.model_validate(c) for c in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get(
    "/{crossing_id}",
    response_model=RailwayCrossingResponse,
    summary="Get crossing details",
)
def get_crossing_endpoint(
    crossing_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
) -> RailwayCrossingResponse:
    crossing = require_entity(
        get_crossing_by_id(db, crossing_id), name="Railway crossing"
    )
    return RailwayCrossingResponse.model_validate(crossing)


@router.patch(
    "/{crossing_id}",
    response_model=RailwayCrossingResponse,
    summary="Update crossing",
)
def update_crossing_endpoint(
    crossing_id: int,
    body: RailwayCrossingUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(CROSSING_WRITE_ROLES))],
) -> RailwayCrossingResponse:
    crossing = update_crossing(
        db,
        crossing_id,
        body,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return RailwayCrossingResponse.model_validate(crossing)


@router.patch(
    "/{crossing_id}/activate",
    response_model=RailwayCrossingResponse,
    summary="Activate crossing",
)
def activate_crossing_endpoint(
    crossing_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(CROSSING_WRITE_ROLES))],
) -> RailwayCrossingResponse:
    crossing = activate_crossing(
        db, crossing_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayCrossingResponse.model_validate(crossing)


@router.patch(
    "/{crossing_id}/deactivate",
    response_model=RailwayCrossingResponse,
    summary="Deactivate crossing",
)
def deactivate_crossing_endpoint(
    crossing_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(CROSSING_WRITE_ROLES))],
) -> RailwayCrossingResponse:
    crossing = deactivate_crossing(
        db, crossing_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayCrossingResponse.model_validate(crossing)


@router.patch(
    "/{crossing_id}/operational-status",
    response_model=RailwayCrossingResponse,
    summary="Update operational status",
)
def update_operational_status_endpoint(
    crossing_id: int,
    body: OperationalStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(CROSSING_STATUS_WRITE_ROLES))],
) -> RailwayCrossingResponse:
    crossing = update_operational_status(
        db,
        crossing_id,
        body.operational_status,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return RailwayCrossingResponse.model_validate(crossing)


@router.patch(
    "/{crossing_id}/monitoring-status",
    response_model=RailwayCrossingResponse,
    summary="Update monitoring status",
)
def update_monitoring_status_endpoint(
    crossing_id: int,
    body: MonitoringStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(CROSSING_STATUS_WRITE_ROLES))],
) -> RailwayCrossingResponse:
    crossing = update_monitoring_status(
        db,
        crossing_id,
        body.monitoring_status,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return RailwayCrossingResponse.model_validate(crossing)
