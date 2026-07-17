"""Railway zone service."""

from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.railway_zone import (
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    VALID_ZONE_STATUSES,
    RailwayZone,
)
from app.schemas.railway_zone import RailwayZoneCreate, RailwayZoneUpdate
from app.services.audit_service import (
    RAILWAY_ZONE_ACTIVATED,
    RAILWAY_ZONE_CREATED,
    RAILWAY_ZONE_DEACTIVATED,
    RAILWAY_ZONE_UPDATED,
    create_audit_log,
)
from app.utils.validation import bad_request, conflict, require_entity, require_valid_choice


def get_zone_by_id(db: Session, zone_id: int) -> Optional[RailwayZone]:
    return db.get(RailwayZone, zone_id)


def get_zone_by_code(db: Session, zone_code: str) -> Optional[RailwayZone]:
    return db.scalar(select(RailwayZone).where(RailwayZone.zone_code == zone_code))


def list_zones(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[list[RailwayZone], int]:
    stmt = select(RailwayZone)
    count_stmt = select(func.count()).select_from(RailwayZone)

    if status is not None:
        stmt = stmt.where(RailwayZone.status == status)
        count_stmt = count_stmt.where(RailwayZone.status == status)
    if is_active is not None:
        stmt = stmt.where(RailwayZone.is_active.is_(is_active))
        count_stmt = count_stmt.where(RailwayZone.is_active.is_(is_active))
    if search:
        pattern = f"%{search}%"
        search_filter = or_(
            RailwayZone.zone_code.ilike(pattern),
            RailwayZone.zone_name.ilike(pattern),
            RailwayZone.headquarters.ilike(pattern),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    total = db.scalar(count_stmt) or 0
    items = list(
        db.scalars(
            stmt.order_by(RailwayZone.zone_code.asc()).offset(skip).limit(limit)
        )
    )
    return items, total


def create_zone(
    db: Session,
    data: RailwayZoneCreate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayZone:
    require_valid_choice(data.status, VALID_ZONE_STATUSES, field_name="status")
    if get_zone_by_code(db, data.zone_code):
        raise conflict(f"Zone code '{data.zone_code}' already exists.")

    zone = RailwayZone(
        zone_code=data.zone_code.strip().upper(),
        zone_name=data.zone_name.strip(),
        headquarters=data.headquarters,
        description=data.description,
        state_coverage=data.state_coverage,
        status=data.status,
        is_active=True,
        created_by_user_id=actor_user_id,
        updated_by_user_id=actor_user_id,
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)

    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_ZONE_CREATED,
        entity_type="railway_zone",
        entity_id=str(zone.id),
        details=f"Zone created: {zone.zone_code} ({zone.zone_name})",
    )
    return zone


def update_zone(
    db: Session,
    zone_id: int,
    data: RailwayZoneUpdate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayZone:
    zone = require_entity(get_zone_by_id(db, zone_id), name="Railway zone")
    assert isinstance(zone, RailwayZone)

    payload = data.model_dump(exclude_unset=True)
    if "status" in payload and payload["status"] is not None:
        require_valid_choice(
            payload["status"], VALID_ZONE_STATUSES, field_name="status"
        )

    for field, value in payload.items():
        setattr(zone, field, value)
    zone.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(zone)

    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_ZONE_UPDATED,
        entity_type="railway_zone",
        entity_id=str(zone.id),
        details=f"Zone updated: {zone.zone_code}",
    )
    return zone


def activate_zone(
    db: Session,
    zone_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayZone:
    zone = require_entity(get_zone_by_id(db, zone_id), name="Railway zone")
    assert isinstance(zone, RailwayZone)
    zone.is_active = True
    zone.status = STATUS_ACTIVE
    zone.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(zone)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_ZONE_ACTIVATED,
        entity_type="railway_zone",
        entity_id=str(zone.id),
        details=f"Zone activated: {zone.zone_code}",
    )
    return zone


def deactivate_zone(
    db: Session,
    zone_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayZone:
    zone = require_entity(get_zone_by_id(db, zone_id), name="Railway zone")
    assert isinstance(zone, RailwayZone)
    zone.is_active = False
    zone.status = STATUS_INACTIVE
    zone.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(zone)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_ZONE_DEACTIVATED,
        entity_type="railway_zone",
        entity_id=str(zone.id),
        details=f"Zone deactivated: {zone.zone_code}",
    )
    return zone
