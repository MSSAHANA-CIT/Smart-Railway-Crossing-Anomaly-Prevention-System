"""Organization hierarchy and crossing overview routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.organization import CrossingOverviewResponse, RailwayHierarchyResponse
from app.services.organization_service import build_hierarchy, get_crossing_overview
from app.services.rbac import ORG_READ_ROLES

router = APIRouter(prefix="/railway", tags=["Organization"])


@router.get(
    "/hierarchy",
    response_model=RailwayHierarchyResponse,
    summary="Get railway organization hierarchy",
)
def get_hierarchy_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    zone_id: Optional[int] = None,
    division_id: Optional[int] = None,
    station_id: Optional[int] = None,
    include_devices: bool = False,
    include_sensors: bool = False,
) -> RailwayHierarchyResponse:
    """
    Return a summary railway hierarchy.

    Devices and sensors are omitted by default to keep responses bounded.
    Live sensor readings are not included in this phase.
    """
    return build_hierarchy(
        db,
        zone_id=zone_id,
        division_id=division_id,
        station_id=station_id,
        include_devices=include_devices,
        include_sensors=include_sensors,
    )


@router.get(
    "/crossings/{crossing_id}/overview",
    response_model=CrossingOverviewResponse,
    summary="Get crossing administrative overview",
)
def get_crossing_overview_endpoint(
    crossing_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
) -> CrossingOverviewResponse:
    """
    Crossing overview with parent hierarchy, devices, and counts.

    Does not include live sensor readings.
    """
    return get_crossing_overview(db, crossing_id)
