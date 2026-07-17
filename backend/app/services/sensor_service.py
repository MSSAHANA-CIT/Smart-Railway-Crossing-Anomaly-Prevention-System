"""Sensor registration service."""

from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.sensor import (
    HEALTH_UNKNOWN,
    SENSOR_STATUS_ACTIVE,
    SENSOR_STATUS_INACTIVE,
    SENSOR_STATUS_REGISTERED,
    VALID_SENSOR_HEALTH_STATUSES,
    VALID_SENSOR_STATUSES,
    Sensor,
)
from app.models.sensor_type import SensorType
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.services.audit_service import (
    SENSOR_ACTIVATED,
    SENSOR_DEACTIVATED,
    SENSOR_HEALTH_STATUS_CHANGED,
    SENSOR_REGISTERED,
    SENSOR_STATUS_CHANGED,
    SENSOR_UPDATED,
    create_audit_log,
)
from app.services.device_service import get_device_by_id
from app.utils.validation import bad_request, conflict, require_entity, require_valid_choice


def get_sensor_by_id(db: Session, sensor_id: int) -> Optional[Sensor]:
    return db.get(Sensor, sensor_id)


def get_sensor_by_code(db: Session, sensor_code: str) -> Optional[Sensor]:
    return db.scalar(select(Sensor).where(Sensor.sensor_code == sensor_code))


def get_sensor_type_by_id(db: Session, sensor_type_id: int) -> Optional[SensorType]:
    return db.get(SensorType, sensor_type_id)


def list_sensors(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    crossing_id: Optional[int] = None,
    device_id: Optional[int] = None,
    sensor_type_id: Optional[int] = None,
    status: Optional[str] = None,
    health_status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[list[Sensor], int]:
    stmt = select(Sensor)
    count_stmt = select(func.count()).select_from(Sensor)

    if crossing_id is not None:
        stmt = stmt.where(Sensor.crossing_id == crossing_id)
        count_stmt = count_stmt.where(Sensor.crossing_id == crossing_id)
    if device_id is not None:
        stmt = stmt.where(Sensor.device_id == device_id)
        count_stmt = count_stmt.where(Sensor.device_id == device_id)
    if sensor_type_id is not None:
        stmt = stmt.where(Sensor.sensor_type_id == sensor_type_id)
        count_stmt = count_stmt.where(Sensor.sensor_type_id == sensor_type_id)
    if status is not None:
        stmt = stmt.where(Sensor.status == status)
        count_stmt = count_stmt.where(Sensor.status == status)
    if health_status is not None:
        stmt = stmt.where(Sensor.health_status == health_status)
        count_stmt = count_stmt.where(Sensor.health_status == health_status)
    if is_active is not None:
        stmt = stmt.where(Sensor.is_active.is_(is_active))
        count_stmt = count_stmt.where(Sensor.is_active.is_(is_active))
    if search:
        pattern = f"%{search}%"
        search_filter = or_(
            Sensor.sensor_code.ilike(pattern),
            Sensor.sensor_name.ilike(pattern),
            Sensor.gpio_reference.ilike(pattern),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    total = db.scalar(count_stmt) or 0
    items = list(
        db.scalars(stmt.order_by(Sensor.sensor_code.asc()).offset(skip).limit(limit))
    )
    return items, total


def register_sensor(
    db: Session,
    data: SensorCreate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Sensor:
    sensor_type = require_entity(
        get_sensor_type_by_id(db, data.sensor_type_id), name="Sensor type"
    )
    assert isinstance(sensor_type, SensorType)
    if not sensor_type.is_active:
        raise bad_request("Sensor type is inactive and cannot be used for registration.")

    device = require_entity(get_device_by_id(db, data.device_id), name="Device")
    assert hasattr(device, "crossing_id")

    if get_sensor_by_code(db, data.sensor_code):
        raise conflict(f"Sensor code '{data.sensor_code}' already exists.")

    crossing_id = data.crossing_id
    if crossing_id is None:
        crossing_id = device.crossing_id
    elif device.crossing_id is not None and crossing_id != device.crossing_id:
        raise bad_request(
            "Sensor crossing_id must match the parent device crossing assignment."
        )

    gpio_reference = data.gpio_reference
    metadata_json = dict(data.metadata_json or {})
    if gpio_reference:
        metadata_json.setdefault(
            "gpio_reference_note",
            "Provisional GPIO label — not a verified hardware mapping.",
        )

    sensor = Sensor(
        sensor_code=data.sensor_code.strip().upper(),
        sensor_name=data.sensor_name.strip(),
        sensor_type_id=data.sensor_type_id,
        device_id=data.device_id,
        crossing_id=crossing_id,
        manufacturer=data.manufacturer,
        model_name=data.model_name,
        unit=data.unit or sensor_type.unit,
        measurement_type=data.measurement_type,
        minimum_value=data.minimum_value,
        maximum_value=data.maximum_value,
        warning_threshold=data.warning_threshold,
        critical_threshold=data.critical_threshold,
        status=SENSOR_STATUS_REGISTERED,
        health_status=HEALTH_UNKNOWN,
        installation_position=data.installation_position,
        gpio_reference=gpio_reference,
        calibration_required=data.calibration_required,
        is_active=True,
        configuration=data.configuration,
        metadata_json=metadata_json or None,
        created_by_user_id=actor_user_id,
        updated_by_user_id=actor_user_id,
    )
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    create_audit_log(
        db,
        actor=actor,
        action=SENSOR_REGISTERED,
        entity_type="sensor",
        entity_id=str(sensor.id),
        details=(
            f"Sensor registered: {sensor.sensor_code} device_id={sensor.device_id} "
            f"(registration does not confirm physical installation)"
        ),
    )
    return sensor


def update_sensor(
    db: Session,
    sensor_id: int,
    data: SensorUpdate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Sensor:
    sensor = require_entity(get_sensor_by_id(db, sensor_id), name="Sensor")
    assert isinstance(sensor, Sensor)

    payload = data.model_dump(exclude_unset=True)
    for field, value in payload.items():
        setattr(sensor, field, value)
    sensor.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(sensor)
    create_audit_log(
        db,
        actor=actor,
        action=SENSOR_UPDATED,
        entity_type="sensor",
        entity_id=str(sensor.id),
        details=f"Sensor updated: {sensor.sensor_code}",
    )
    return sensor


def update_sensor_status(
    db: Session,
    sensor_id: int,
    status: str,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Sensor:
    sensor = require_entity(get_sensor_by_id(db, sensor_id), name="Sensor")
    assert isinstance(sensor, Sensor)
    require_valid_choice(status, VALID_SENSOR_STATUSES, field_name="status")
    previous = sensor.status
    sensor.status = status
    sensor.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(sensor)
    create_audit_log(
        db,
        actor=actor,
        action=SENSOR_STATUS_CHANGED,
        entity_type="sensor",
        entity_id=str(sensor.id),
        details=f"Sensor status: {previous} -> {status} ({sensor.sensor_code})",
    )
    return sensor


def update_sensor_health_status(
    db: Session,
    sensor_id: int,
    health_status: str,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Sensor:
    sensor = require_entity(get_sensor_by_id(db, sensor_id), name="Sensor")
    assert isinstance(sensor, Sensor)
    require_valid_choice(
        health_status, VALID_SENSOR_HEALTH_STATUSES, field_name="health_status"
    )
    previous = sensor.health_status
    sensor.health_status = health_status
    sensor.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(sensor)
    create_audit_log(
        db,
        actor=actor,
        action=SENSOR_HEALTH_STATUS_CHANGED,
        entity_type="sensor",
        entity_id=str(sensor.id),
        details=(
            f"Sensor health: {previous} -> {health_status} ({sensor.sensor_code})"
        ),
    )
    return sensor


def activate_sensor(
    db: Session,
    sensor_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Sensor:
    sensor = require_entity(get_sensor_by_id(db, sensor_id), name="Sensor")
    assert isinstance(sensor, Sensor)
    sensor.is_active = True
    sensor.status = SENSOR_STATUS_ACTIVE
    sensor.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(sensor)
    create_audit_log(
        db,
        actor=actor,
        action=SENSOR_ACTIVATED,
        entity_type="sensor",
        entity_id=str(sensor.id),
        details=f"Sensor activated: {sensor.sensor_code}",
    )
    return sensor


def deactivate_sensor(
    db: Session,
    sensor_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Sensor:
    sensor = require_entity(get_sensor_by_id(db, sensor_id), name="Sensor")
    assert isinstance(sensor, Sensor)
    sensor.is_active = False
    sensor.status = SENSOR_STATUS_INACTIVE
    sensor.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(sensor)
    create_audit_log(
        db,
        actor=actor,
        action=SENSOR_DEACTIVATED,
        entity_type="sensor",
        entity_id=str(sensor.id),
        details=f"Sensor deactivated: {sensor.sensor_code}",
    )
    return sensor
