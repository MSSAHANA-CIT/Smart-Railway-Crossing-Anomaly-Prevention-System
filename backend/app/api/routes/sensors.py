"""Sensor management routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.pagination import PaginatedResponse
from app.schemas.sensor import (
    SensorCreate,
    SensorHealthStatusUpdate,
    SensorResponse,
    SensorStatusUpdate,
    SensorUpdate,
)
from app.services.rbac import ORG_READ_ROLES, SENSOR_MAINTENANCE_ROLES, SENSOR_WRITE_ROLES
from app.services.sensor_service import (
    activate_sensor,
    deactivate_sensor,
    get_sensor_by_id,
    list_sensors,
    register_sensor,
    update_sensor,
    update_sensor_health_status,
    update_sensor_status,
)
from app.utils.pagination import PaginationParams, build_paginated_response, pagination_params
from app.utils.validation import require_entity

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post(
    "",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register sensor",
)
def register_sensor_endpoint(
    body: SensorCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(SENSOR_WRITE_ROLES))],
) -> SensorResponse:
    """
    Register a planned sensor under a device.

    Registration does not confirm physical installation or verified GPIO mapping.
    """
    sensor = register_sensor(
        db, body, actor=current_user.email, actor_user_id=current_user.id
    )
    return SensorResponse.model_validate(sensor)


@router.get(
    "",
    response_model=PaginatedResponse[SensorResponse],
    summary="List sensors",
)
def list_sensors_endpoint(
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
    pagination: Annotated[PaginationParams, Depends(pagination_params)],
    crossing_id: Optional[int] = None,
    device_id: Optional[int] = None,
    sensor_type_id: Optional[int] = None,
    status_filter: Annotated[Optional[str], Query(alias="status")] = None,
    health_status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> PaginatedResponse[SensorResponse]:
    items, total = list_sensors(
        db,
        skip=pagination.skip,
        limit=pagination.limit,
        crossing_id=crossing_id,
        device_id=device_id,
        sensor_type_id=sensor_type_id,
        status=status_filter,
        health_status=health_status,
        is_active=is_active,
        search=search,
    )
    return build_paginated_response(
        [SensorResponse.model_validate(s) for s in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{sensor_id}", response_model=SensorResponse, summary="Get sensor details")
def get_sensor_endpoint(
    sensor_id: int,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[User, Depends(require_roles(ORG_READ_ROLES))],
) -> SensorResponse:
    sensor = require_entity(get_sensor_by_id(db, sensor_id), name="Sensor")
    return SensorResponse.model_validate(sensor)


@router.patch("/{sensor_id}", response_model=SensorResponse, summary="Update sensor")
def update_sensor_endpoint(
    sensor_id: int,
    body: SensorUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(SENSOR_WRITE_ROLES))],
) -> SensorResponse:
    sensor = update_sensor(
        db,
        sensor_id,
        body,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return SensorResponse.model_validate(sensor)


@router.patch(
    "/{sensor_id}/status",
    response_model=SensorResponse,
    summary="Update sensor status",
)
def update_sensor_status_endpoint(
    sensor_id: int,
    body: SensorStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(SENSOR_MAINTENANCE_ROLES))],
) -> SensorResponse:
    sensor = update_sensor_status(
        db,
        sensor_id,
        body.status,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return SensorResponse.model_validate(sensor)


@router.patch(
    "/{sensor_id}/health-status",
    response_model=SensorResponse,
    summary="Update sensor health status",
)
def update_sensor_health_endpoint(
    sensor_id: int,
    body: SensorHealthStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(SENSOR_MAINTENANCE_ROLES))],
) -> SensorResponse:
    sensor = update_sensor_health_status(
        db,
        sensor_id,
        body.health_status,
        actor=current_user.email,
        actor_user_id=current_user.id,
    )
    return SensorResponse.model_validate(sensor)


@router.patch(
    "/{sensor_id}/activate",
    response_model=SensorResponse,
    summary="Activate sensor",
)
def activate_sensor_endpoint(
    sensor_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(SENSOR_WRITE_ROLES))],
) -> SensorResponse:
    sensor = activate_sensor(
        db, sensor_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return SensorResponse.model_validate(sensor)


@router.patch(
    "/{sensor_id}/deactivate",
    response_model=SensorResponse,
    summary="Deactivate sensor",
)
def deactivate_sensor_endpoint(
    sensor_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_roles(SENSOR_WRITE_ROLES))],
) -> SensorResponse:
    sensor = deactivate_sensor(
        db, sensor_id, actor=current_user.email, actor_user_id=current_user.id
    )
    return SensorResponse.model_validate(sensor)
