"""Device registration and crossing assignment service."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.device import (
    DEVICE_STATUS_ACTIVE,
    DEVICE_STATUS_INACTIVE,
    DEVICE_STATUS_REGISTERED,
    HEALTH_UNKNOWN,
    VALID_COMMUNICATION_TYPES,
    VALID_DEVICE_STATUSES,
    VALID_DEVICE_TYPES,
    VALID_HEALTH_STATUSES,
    Device,
)
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.services.audit_service import (
    DEVICE_ACTIVATED,
    DEVICE_ASSIGNED,
    DEVICE_DEACTIVATED,
    DEVICE_HEALTH_STATUS_CHANGED,
    DEVICE_REGISTERED,
    DEVICE_STATUS_CHANGED,
    DEVICE_UNASSIGNED,
    DEVICE_UPDATED,
    create_audit_log,
)
from app.services.railway_crossing_service import get_crossing_by_id
from app.utils.validation import bad_request, conflict, require_entity, require_valid_choice


def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
    return db.get(Device, device_id)


def get_device_by_code(db: Session, device_code: str) -> Optional[Device]:
    return db.scalar(select(Device).where(Device.device_code == device_code))


def _normalize_optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _ensure_unique_serial(db: Session, serial_number: Optional[str], *, exclude_id: Optional[int] = None) -> None:
    serial_number = _normalize_optional(serial_number)
    if not serial_number:
        return
    stmt = select(Device).where(Device.serial_number == serial_number)
    if exclude_id is not None:
        stmt = stmt.where(Device.id != exclude_id)
    if db.scalar(stmt):
        raise conflict(f"Serial number '{serial_number}' is already registered.")


def _ensure_unique_mac(db: Session, mac_address: Optional[str], *, exclude_id: Optional[int] = None) -> None:
    mac_address = _normalize_optional(mac_address)
    if not mac_address:
        return
    stmt = select(Device).where(Device.mac_address == mac_address)
    if exclude_id is not None:
        stmt = stmt.where(Device.id != exclude_id)
    if db.scalar(stmt):
        raise conflict(f"MAC address '{mac_address}' is already registered.")


def list_devices(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    crossing_id: Optional[int] = None,
    device_type: Optional[str] = None,
    status: Optional[str] = None,
    health_status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[list[Device], int]:
    stmt = select(Device)
    count_stmt = select(func.count()).select_from(Device)

    if crossing_id is not None:
        stmt = stmt.where(Device.crossing_id == crossing_id)
        count_stmt = count_stmt.where(Device.crossing_id == crossing_id)
    if device_type is not None:
        stmt = stmt.where(Device.device_type == device_type)
        count_stmt = count_stmt.where(Device.device_type == device_type)
    if status is not None:
        stmt = stmt.where(Device.status == status)
        count_stmt = count_stmt.where(Device.status == status)
    if health_status is not None:
        stmt = stmt.where(Device.health_status == health_status)
        count_stmt = count_stmt.where(Device.health_status == health_status)
    if is_active is not None:
        stmt = stmt.where(Device.is_active.is_(is_active))
        count_stmt = count_stmt.where(Device.is_active.is_(is_active))
    if search:
        pattern = f"%{search}%"
        search_filter = or_(
            Device.device_code.ilike(pattern),
            Device.device_name.ilike(pattern),
            Device.serial_number.ilike(pattern),
            Device.mac_address.ilike(pattern),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    total = db.scalar(count_stmt) or 0
    items = list(
        db.scalars(stmt.order_by(Device.device_code.asc()).offset(skip).limit(limit))
    )
    return items, total


def register_device(
    db: Session,
    data: DeviceCreate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Device:
    require_valid_choice(data.device_type, VALID_DEVICE_TYPES, field_name="device_type")
    require_valid_choice(
        data.communication_type,
        VALID_COMMUNICATION_TYPES,
        field_name="communication_type",
    )
    if get_device_by_code(db, data.device_code):
        raise conflict(f"Device code '{data.device_code}' already exists.")

    serial_number = _normalize_optional(data.serial_number)
    mac_address = _normalize_optional(data.mac_address)
    _ensure_unique_serial(db, serial_number)
    _ensure_unique_mac(db, mac_address)

    crossing_id = data.crossing_id
    if crossing_id is not None:
        require_entity(get_crossing_by_id(db, crossing_id), name="Railway crossing")

    now = datetime.now(timezone.utc)
    device = Device(
        device_code=data.device_code.strip().upper(),
        device_name=data.device_name.strip(),
        device_type=data.device_type,
        serial_number=serial_number,
        manufacturer=data.manufacturer,
        model_name=data.model_name,
        hardware_version=data.hardware_version,
        firmware_version=data.firmware_version,
        crossing_id=crossing_id,
        installation_location=data.installation_location,
        location=data.installation_location,
        mac_address=mac_address,
        ip_address=_normalize_optional(data.ip_address),
        communication_type=data.communication_type,
        status=DEVICE_STATUS_REGISTERED,
        health_status=HEALTH_UNKNOWN,
        registered_at=now,
        is_active=True,
        configuration=data.configuration,
        metadata_json=data.metadata_json,
        created_by_user_id=actor_user_id,
        updated_by_user_id=actor_user_id,
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    create_audit_log(
        db,
        actor=actor,
        action=DEVICE_REGISTERED,
        entity_type="device",
        entity_id=str(device.id),
        details=(
            f"Device registered: {device.device_code} type={device.device_type} "
            f"health={device.health_status}"
        ),
    )
    return device


def update_device(
    db: Session,
    device_id: int,
    data: DeviceUpdate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Device:
    device = require_entity(get_device_by_id(db, device_id), name="Device")
    assert isinstance(device, Device)

    payload = data.model_dump(exclude_unset=True)
    if "device_type" in payload and payload["device_type"] is not None:
        require_valid_choice(
            payload["device_type"], VALID_DEVICE_TYPES, field_name="device_type"
        )
    if "communication_type" in payload and payload["communication_type"] is not None:
        require_valid_choice(
            payload["communication_type"],
            VALID_COMMUNICATION_TYPES,
            field_name="communication_type",
        )
    if "serial_number" in payload:
        serial = _normalize_optional(payload["serial_number"])
        _ensure_unique_serial(db, serial, exclude_id=device.id)
        payload["serial_number"] = serial
    if "mac_address" in payload:
        mac = _normalize_optional(payload["mac_address"])
        _ensure_unique_mac(db, mac, exclude_id=device.id)
        payload["mac_address"] = mac

    for field, value in payload.items():
        setattr(device, field, value)
    if "installation_location" in payload:
        device.location = payload["installation_location"]
    device.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(device)
    create_audit_log(
        db,
        actor=actor,
        action=DEVICE_UPDATED,
        entity_type="device",
        entity_id=str(device.id),
        details=f"Device updated: {device.device_code}",
    )
    return device


def assign_device_to_crossing(
    db: Session,
    device_id: int,
    crossing_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Device:
    device = require_entity(get_device_by_id(db, device_id), name="Device")
    assert isinstance(device, Device)
    require_entity(get_crossing_by_id(db, crossing_id), name="Railway crossing")

    if device.crossing_id is not None and device.crossing_id != crossing_id:
        raise conflict(
            "Device is already assigned to another crossing. Unassign it first."
        )
    if device.crossing_id == crossing_id:
        return device

    device.crossing_id = crossing_id
    device.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(device)
    create_audit_log(
        db,
        actor=actor,
        action=DEVICE_ASSIGNED,
        entity_type="device",
        entity_id=str(device.id),
        details=f"Device {device.device_code} assigned to crossing_id={crossing_id}",
    )
    return device


def unassign_device(
    db: Session,
    device_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Device:
    device = require_entity(get_device_by_id(db, device_id), name="Device")
    assert isinstance(device, Device)
    previous = device.crossing_id
    device.crossing_id = None
    device.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(device)
    create_audit_log(
        db,
        actor=actor,
        action=DEVICE_UNASSIGNED,
        entity_type="device",
        entity_id=str(device.id),
        details=(
            f"Device {device.device_code} unassigned from crossing_id={previous}"
        ),
    )
    return device


def update_device_status(
    db: Session,
    device_id: int,
    status: str,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Device:
    device = require_entity(get_device_by_id(db, device_id), name="Device")
    assert isinstance(device, Device)
    require_valid_choice(status, VALID_DEVICE_STATUSES, field_name="status")
    previous = device.status
    device.status = status
    device.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(device)
    create_audit_log(
        db,
        actor=actor,
        action=DEVICE_STATUS_CHANGED,
        entity_type="device",
        entity_id=str(device.id),
        details=f"Device status: {previous} -> {status} ({device.device_code})",
    )
    return device


def update_device_health_status(
    db: Session,
    device_id: int,
    health_status: str,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Device:
    device = require_entity(get_device_by_id(db, device_id), name="Device")
    assert isinstance(device, Device)
    require_valid_choice(
        health_status, VALID_HEALTH_STATUSES, field_name="health_status"
    )
    previous = device.health_status
    device.health_status = health_status
    device.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(device)
    create_audit_log(
        db,
        actor=actor,
        action=DEVICE_HEALTH_STATUS_CHANGED,
        entity_type="device",
        entity_id=str(device.id),
        details=(
            f"Device health: {previous} -> {health_status} ({device.device_code})"
        ),
    )
    return device


def activate_device(
    db: Session,
    device_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Device:
    device = require_entity(get_device_by_id(db, device_id), name="Device")
    assert isinstance(device, Device)
    device.is_active = True
    device.status = DEVICE_STATUS_ACTIVE
    device.activated_at = datetime.now(timezone.utc)
    device.deactivated_at = None
    device.updated_by_user_id = actor_user_id
    # Activation does not imply HEALTHY — health remains until real telemetry
    db.commit()
    db.refresh(device)
    create_audit_log(
        db,
        actor=actor,
        action=DEVICE_ACTIVATED,
        entity_type="device",
        entity_id=str(device.id),
        details=f"Device activated: {device.device_code} health={device.health_status}",
    )
    return device


def deactivate_device(
    db: Session,
    device_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> Device:
    device = require_entity(get_device_by_id(db, device_id), name="Device")
    assert isinstance(device, Device)
    device.is_active = False
    device.status = DEVICE_STATUS_INACTIVE
    device.deactivated_at = datetime.now(timezone.utc)
    device.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(device)
    create_audit_log(
        db,
        actor=actor,
        action=DEVICE_DEACTIVATED,
        entity_type="device",
        entity_id=str(device.id),
        details=f"Device deactivated: {device.device_code}",
    )
    return device
