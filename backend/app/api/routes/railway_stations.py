"""Railway station management routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.pagination import PaginatedResponse
from app.schemas.railway_station import (
    RailwayStationCreate,
    RailwayStationResponse,
    RailwayStationUpdate,
)
from app.services.rbac import ORG_READ_ROLES, STATION_WRITE_ROLES
from app.services.railway_station_service import (
    activate_station,
    create_station,
    deactivate_station,
    get_station_by_id,
    list_stations,
    update_station,
)
from app.utils.pagination import PaginationParams, build_paginated_response, pagination_params
from app.utils.validation import require_entity

router = APIRouter(prefix="/railway/stations", tags=["Railway Stations"])


@router.post(
    "",
    response_model=RailwayStationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create railway station",
)
def create_station_endpoint(
    body: RailwayStationCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(STATION_WRITE_ROLES))],
) -> RailwayStationResponse:
    """Create a station under a division. Validates parent division."""
    station = create_station(
        db, body, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayStationResponse.model_validate(station)


@router.get(
    "",
    response_model=PaginatedResponse[RailwayStationResponse],
    summary="List railway stations",
)
def list_stations_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    division_id: Optional[int] = None,
    zone_id: Optional[int] = None,
    state: Optional[str] = None,
    station_type: Optional[str] = None,
    status_filter: Annotated[Optional[str], Query(alias="status")] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> PaginatedResponse[RailwayStationResponse]:
    items, total = list_stations(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        division_id=division_id,
        zone_id=zone_id,
        state=state,
        station_type=station_type,
        status=status_filter,
        is_active=is_active,
        search=search,
    )
    return build_paginated_response(
        [RailwayStationResponse.model_validate(s) for s in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get(
    "/{station_id}",
    response_model=RailwayStationResponse,
    summary="Get station details",
)
def get_station_endpoint(
    station_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
) -> RailwayStationResponse:
    station = require_entity(
        get_station_by_id(db, station_id), name="Railway station"
    )
    return RailwayStationResponse.model_validate(station)


@router.patch(
    "/{station_id}",
    response_model=RailwayStationResponse,
    summary="Update station",
)
def update_station_endpoint(
    station_id: int,
    body: RailwayStationUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(STATION_WRITE_ROLES))],
) -> RailwayStationResponse:
    station = update_station(
        db,
        station_id,
        body,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return RailwayStationResponse.model_validate(station)


@router.patch(
    "/{station_id}/activate",
    response_model=RailwayStationResponse,
    summary="Activate station",
)
def activate_station_endpoint(
    station_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(STATION_WRITE_ROLES))],
) -> RailwayStationResponse:
    station = activate_station(
        db, station_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayStationResponse.model_validate(station)


@router.patch(
    "/{station_id}/deactivate",
    response_model=RailwayStationResponse,
    summary="Deactivate station",
)
def deactivate_station_endpoint(
    station_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(STATION_WRITE_ROLES))],
) -> RailwayStationResponse:
    station = deactivate_station(
        db, station_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayStationResponse.model_validate(station)
