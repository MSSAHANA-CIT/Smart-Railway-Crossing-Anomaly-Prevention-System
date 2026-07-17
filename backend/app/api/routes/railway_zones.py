"""Railway zone management routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.railway_zone import (
    RailwayZoneCreate,
    RailwayZoneResponse,
    RailwayZoneUpdate,
)
from app.schemas.pagination import PaginatedResponse
from app.services.rbac import ORG_READ_ROLES, ZONE_WRITE_ROLES
from app.services.railway_zone_service import (
    activate_zone,
    create_zone,
    deactivate_zone,
    get_zone_by_id,
    list_zones,
    update_zone,
)
from app.utils.pagination import PaginationParams, build_paginated_response, pagination_params
from app.utils.validation import require_entity

router = APIRouter(prefix="/railway/zones", tags=["Railway Zones"])


@router.post(
    "",
    response_model=RailwayZoneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create railway zone",
)
def create_zone_endpoint(
    body: RailwayZoneCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(ZONE_WRITE_ROLES))],
) -> RailwayZoneResponse:
    """Create a railway zone. Requires SUPER_ADMIN or RAILWAY_ADMIN."""
    zone = create_zone(
        db, body, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayZoneResponse.model_validate(zone)


@router.get(
    "",
    response_model=PaginatedResponse[RailwayZoneResponse],
    summary="List railway zones",
)
def list_zones_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    status_filter: Annotated[Optional[str], Query(alias="status")] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> PaginatedResponse[RailwayZoneResponse]:
    """List zones with pagination and filters. Requires authenticated railway role."""
    items, total = list_zones(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        status=status_filter,
        is_active=is_active,
        search=search,
    )
    return build_paginated_response(
        [RailwayZoneResponse.model_validate(z) for z in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{zone_id}", response_model=RailwayZoneResponse, summary="Get zone details")
def get_zone_endpoint(
    zone_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
) -> RailwayZoneResponse:
    zone = require_entity(get_zone_by_id(db, zone_id), name="Railway zone")
    return RailwayZoneResponse.model_validate(zone)


@router.patch("/{zone_id}", response_model=RailwayZoneResponse, summary="Update zone")
def update_zone_endpoint(
    zone_id: int,
    body: RailwayZoneUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(ZONE_WRITE_ROLES))],
) -> RailwayZoneResponse:
    zone = update_zone(
        db,
        zone_id,
        body,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return RailwayZoneResponse.model_validate(zone)


@router.patch(
    "/{zone_id}/activate",
    response_model=RailwayZoneResponse,
    summary="Activate zone",
)
def activate_zone_endpoint(
    zone_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(ZONE_WRITE_ROLES))],
) -> RailwayZoneResponse:
    zone = activate_zone(
        db, zone_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayZoneResponse.model_validate(zone)


@router.patch(
    "/{zone_id}/deactivate",
    response_model=RailwayZoneResponse,
    summary="Deactivate zone",
)
def deactivate_zone_endpoint(
    zone_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(ZONE_WRITE_ROLES))],
) -> RailwayZoneResponse:
    """Soft-deactivate a zone. Physical deletion is not supported."""
    zone = deactivate_zone(
        db, zone_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return RailwayZoneResponse.model_validate(zone)
