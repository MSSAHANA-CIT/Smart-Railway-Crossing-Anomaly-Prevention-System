"""Device management routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.device import (
    DeviceAssignmentRequest,
    DeviceCreate,
    DeviceHealthStatusUpdate,
    DeviceResponse,
    DeviceStatusUpdate,
    DeviceUpdate,
)
from app.schemas.pagination import PaginatedResponse
from app.schemas.sensor import SensorResponse
from app.services.device_service import (
    activate_device,
    assign_device_to_crossing,
    deactivate_device,
    get_device_by_id,
    list_devices,
    register_device,
    unassign_device,
    update_device,
    update_device_health_status,
    update_device_status,
)
from app.services.rbac import (
    DEVICE_MAINTENANCE_ROLES,
    DEVICE_WRITE_ROLES,
    ORG_READ_ROLES,
)
from app.services.sensor_service import list_sensors
from app.utils.pagination import PaginationParams, build_paginated_response, pagination_params
from app.utils.validation import require_entity

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register device",
)
def register_device_endpoint(
    body: DeviceCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DEVICE_WRITE_ROLES))],
) -> DeviceResponse:
    """
    Register a hardware or simulated device.

    Health status defaults to UNKNOWN — registration does not imply healthy hardware.
    """
    device = register_device(
        db, body, actor=current_user.email, actor_user_id=current_user.id
    )
    return DeviceResponse.model_validate(device)


@router.get(
    "",
    response_model=PaginatedResponse[DeviceResponse],
    summary="List devices",
)
def list_devices_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    crossing_id: Optional[int] = None,
    device_type: Optional[str] = None,
    status_filter: Annotated[Optional[str], Query(alias="status")] = None,
    health_status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> PaginatedResponse[DeviceResponse]:
    items, total = list_devices(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        crossing_id=crossing_id,
        device_type=device_type,
        status=status_filter,
        health_status=health_status,
        is_active=is_active,
        search=search,
    )
    return build_paginated_response(
        [DeviceResponse.model_validate(d) for d in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{device_id}", response_model=DeviceResponse, summary="Get device details")
def get_device_endpoint(
    device_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
) -> DeviceResponse:
    device = require_entity(get_device_by_id(db, device_id), name="Device")
    return DeviceResponse.model_validate(device)


@router.patch("/{device_id}", response_model=DeviceResponse, summary="Update device")
def update_device_endpoint(
    device_id: int,
    body: DeviceUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DEVICE_WRITE_ROLES))],
) -> DeviceResponse:
    device = update_device(
        db,
        device_id,
        body,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return DeviceResponse.model_validate(device)


@router.post(
    "/{device_id}/assign",
    response_model=DeviceResponse,
    summary="Assign device to crossing",
)
def assign_device_endpoint(
    device_id: int,
    body: DeviceAssignmentRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DEVICE_WRITE_ROLES))],
) -> DeviceResponse:
    """Assign device to a crossing. A device may belong to at most one crossing."""
    device = assign_device_to_crossing(
        db,
        device_id,
        body.crossing_id,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return DeviceResponse.model_validate(device)


@router.post(
    "/{device_id}/unassign",
    response_model=DeviceResponse,
    summary="Unassign device from crossing",
)
def unassign_device_endpoint(
    device_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DEVICE_WRITE_ROLES))],
) -> DeviceResponse:
    """Remove crossing assignment while preserving the device record."""
    device = unassign_device(
        db, device_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return DeviceResponse.model_validate(device)


@router.patch(
    "/{device_id}/status",
    response_model=DeviceResponse,
    summary="Update device status",
)
def update_device_status_endpoint(
    device_id: int,
    body: DeviceStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DEVICE_MAINTENANCE_ROLES))],
) -> DeviceResponse:
    device = update_device_status(
        db,
        device_id,
        body.status,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return DeviceResponse.model_validate(device)


@router.patch(
    "/{device_id}/health-status",
    response_model=DeviceResponse,
    summary="Update device health status",
)
def update_device_health_endpoint(
    device_id: int,
    body: DeviceHealthStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DEVICE_MAINTENANCE_ROLES))],
) -> DeviceResponse:
    """Manual health update for prototype/admin use. Future phases add heartbeats."""
    device = update_device_health_status(
        db,
        device_id,
        body.health_status,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return DeviceResponse.model_validate(device)


@router.patch(
    "/{device_id}/activate",
    response_model=DeviceResponse,
    summary="Activate device",
)
def activate_device_endpoint(
    device_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DEVICE_WRITE_ROLES))],
) -> DeviceResponse:
    device = activate_device(
        db, device_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return DeviceResponse.model_validate(device)


@router.patch(
    "/{device_id}/deactivate",
    response_model=DeviceResponse,
    summary="Deactivate device",
)
def deactivate_device_endpoint(
    device_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(DEVICE_WRITE_ROLES))],
) -> DeviceResponse:
    device = deactivate_device(
        db, device_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return DeviceResponse.model_validate(device)


@router.get(
    "/{device_id}/sensors",
    response_model=PaginatedResponse[SensorResponse],
    summary="List sensors for a device",
)
def list_device_sensors_endpoint(
    device_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
) -> PaginatedResponse[SensorResponse]:
    require_entity(get_device_by_id(db, device_id), name="Device")
    items, total = list_sensors(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        device_id=device_id,
    )
    return build_paginated_response(
        [SensorResponse.model_validate(s) for s in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )
