"""Railway crossing service with hierarchy integrity validation."""

from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.railway_crossing import (
    VALID_CROSSING_TYPES,
    VALID_GATE_TYPES,
    VALID_MONITORING_STATUSES,
    VALID_OPERATIONAL_STATUSES,
    VALID_RISK_CATEGORIES,
    RailwayCrossing,
)
from app.schemas.railway_crossing import RailwayCrossingCreate, RailwayCrossingUpdate
from app.services.audit_service import (
    RAILWAY_CROSSING_ACTIVATED,
    RAILWAY_CROSSING_CREATED,
    RAILWAY_CROSSING_DEACTIVATED,
    RAILWAY_CROSSING_STATUS_CHANGED,
    RAILWAY_CROSSING_UPDATED,
    create_audit_log,
)
from app.services.railway_division_service import get_division_by_id
from app.services.railway_station_service import get_station_by_id
from app.services.railway_zone_service import get_zone_by_id
from app.utils.validation import bad_request, conflict, require_entity, require_valid_choice


def get_crossing_by_id(db: Session, crossing_id: int) -> Optional[RailwayCrossing]:
    return db.get(RailwayCrossing, crossing_id)


def get_crossing_by_code(
    db: Session, crossing_code: str
) -> Optional[RailwayCrossing]:
    return db.scalar(
        select(RailwayCrossing).where(RailwayCrossing.crossing_code == crossing_code)
    )


def validate_crossing_hierarchy(
    db: Session,
    *,
    station_id: int,
    division_id: int,
    zone_id: int,
) -> None:
    """Ensure station → division → zone relationships are consistent."""
    zone = require_entity(get_zone_by_id(db, zone_id), name="Parent railway zone")
    division = require_entity(
        get_division_by_id(db, division_id), name="Parent railway division"
    )
    station = require_entity(
        get_station_by_id(db, station_id), name="Parent railway station"
    )

    assert hasattr(division, "zone_id")
    assert hasattr(station, "division_id")

    if division.zone_id != zone_id:
        raise bad_request(
            "Invalid hierarchy: division does not belong to the provided zone."
        )
    if station.division_id != division_id:
        raise bad_request(
            "Invalid hierarchy: station does not belong to the provided division."
        )
    # Silence unused after assert for type checkers
    _ = zone


def list_crossings(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    zone_id: Optional[int] = None,
    division_id: Optional[int] = None,
    station_id: Optional[int] = None,
    crossing_type: Optional[str] = None,
    operational_status: Optional[str] = None,
    monitoring_status: Optional[str] = None,
    risk_category: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[list[RailwayCrossing], int]:
    stmt = select(RailwayCrossing)
    count_stmt = select(func.count()).select_from(RailwayCrossing)

    filters = {
        "zone_id": zone_id,
        "division_id": division_id,
        "station_id": station_id,
        "crossing_type": crossing_type,
        "operational_status": operational_status,
        "monitoring_status": monitoring_status,
        "risk_category": risk_category,
    }
    for attr, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(RailwayCrossing, attr) == value)
            count_stmt = count_stmt.where(getattr(RailwayCrossing, attr) == value)

    if is_active is not None:
        stmt = stmt.where(RailwayCrossing.is_active.is_(is_active))
        count_stmt = count_stmt.where(RailwayCrossing.is_active.is_(is_active))
    if search:
        pattern = f"%{search}%"
        search_filter = or_(
            RailwayCrossing.crossing_code.ilike(pattern),
            RailwayCrossing.crossing_name.ilike(pattern),
            RailwayCrossing.road_name.ilike(pattern),
            RailwayCrossing.landmark.ilike(pattern),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    total = db.scalar(count_stmt) or 0
    items = list(
        db.scalars(
            stmt.order_by(RailwayCrossing.crossing_code.asc())
            .offset(skip)
            .limit(limit)
        )
    )
    return items, total


def create_crossing(
    db: Session,
    data: RailwayCrossingCreate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayCrossing:
    require_valid_choice(
        data.crossing_type, VALID_CROSSING_TYPES, field_name="crossing_type"
    )
    require_valid_choice(data.gate_type, VALID_GATE_TYPES, field_name="gate_type")
    require_valid_choice(
        data.risk_category, VALID_RISK_CATEGORIES, field_name="risk_category"
    )
    require_valid_choice(
        data.operational_status,
        VALID_OPERATIONAL_STATUSES,
        field_name="operational_status",
    )
    require_valid_choice(
        data.monitoring_status,
        VALID_MONITORING_STATUSES,
        field_name="monitoring_status",
    )
    validate_crossing_hierarchy(
        db,
        station_id=data.station_id,
        division_id=data.division_id,
        zone_id=data.zone_id,
    )
    if get_crossing_by_code(db, data.crossing_code):
        raise conflict(f"Crossing code '{data.crossing_code}' already exists.")

    location = data.location or data.road_name or data.landmark or data.crossing_name

    crossing = RailwayCrossing(
        crossing_code=data.crossing_code.strip().upper(),
        crossing_name=data.crossing_name.strip(),
        location=location,
        station_id=data.station_id,
        division_id=data.division_id,
        zone_id=data.zone_id,
        crossing_type=data.crossing_type,
        road_name=data.road_name,
        landmark=data.landmark,
        latitude=data.latitude,
        longitude=data.longitude,
        gate_type=data.gate_type,
        number_of_tracks=data.number_of_tracks,
        risk_category=data.risk_category,
        operational_status=data.operational_status,
        monitoring_status=data.monitoring_status,
        description=data.description,
        is_active=True,
        status="active",
        created_by_user_id=actor_user_id,
        updated_by_user_id=actor_user_id,
    )
    db.add(crossing)
    db.commit()
    db.refresh(crossing)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_CROSSING_CREATED,
        entity_type="railway_crossing",
        entity_id=str(crossing.id),
        details=(
            f"Crossing created: {crossing.crossing_code} "
            f"station_id={crossing.station_id}"
        ),
    )
    return crossing


def update_crossing(
    db: Session,
    crossing_id: int,
    data: RailwayCrossingUpdate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayCrossing:
    crossing = require_entity(
        get_crossing_by_id(db, crossing_id), name="Railway crossing"
    )
    assert isinstance(crossing, RailwayCrossing)

    payload = data.model_dump(exclude_unset=True)
    validators = {
        "crossing_type": VALID_CROSSING_TYPES,
        "gate_type": VALID_GATE_TYPES,
        "risk_category": VALID_RISK_CATEGORIES,
        "operational_status": VALID_OPERATIONAL_STATUSES,
        "monitoring_status": VALID_MONITORING_STATUSES,
    }
    for field, valid in validators.items():
        if field in payload and payload[field] is not None:
            require_valid_choice(payload[field], valid, field_name=field)

    station_id = payload.get("station_id", crossing.station_id)
    division_id = payload.get("division_id", crossing.division_id)
    zone_id = payload.get("zone_id", crossing.zone_id)
    if station_id is None or division_id is None or zone_id is None:
        raise bad_request(
            "Crossing hierarchy fields station_id, division_id, and zone_id are required."
        )
    validate_crossing_hierarchy(
        db,
        station_id=station_id,
        division_id=division_id,
        zone_id=zone_id,
    )

    for field, value in payload.items():
        setattr(crossing, field, value)
    crossing.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(crossing)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_CROSSING_UPDATED,
        entity_type="railway_crossing",
        entity_id=str(crossing.id),
        details=f"Crossing updated: {crossing.crossing_code}",
    )
    return crossing


def update_operational_status(
    db: Session,
    crossing_id: int,
    operational_status: str,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayCrossing:
    crossing = require_entity(
        get_crossing_by_id(db, crossing_id), name="Railway crossing"
    )
    assert isinstance(crossing, RailwayCrossing)
    require_valid_choice(
        operational_status,
        VALID_OPERATIONAL_STATUSES,
        field_name="operational_status",
    )
    previous = crossing.operational_status
    crossing.operational_status = operational_status
    crossing.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(crossing)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_CROSSING_STATUS_CHANGED,
        entity_type="railway_crossing",
        entity_id=str(crossing.id),
        details=(
            f"Operational status changed: {previous} -> {operational_status} "
            f"({crossing.crossing_code})"
        ),
    )
    return crossing


def update_monitoring_status(
    db: Session,
    crossing_id: int,
    monitoring_status: str,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayCrossing:
    crossing = require_entity(
        get_crossing_by_id(db, crossing_id), name="Railway crossing"
    )
    assert isinstance(crossing, RailwayCrossing)
    require_valid_choice(
        monitoring_status,
        VALID_MONITORING_STATUSES,
        field_name="monitoring_status",
    )
    previous = crossing.monitoring_status
    crossing.monitoring_status = monitoring_status
    crossing.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(crossing)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_CROSSING_STATUS_CHANGED,
        entity_type="railway_crossing",
        entity_id=str(crossing.id),
        details=(
            f"Monitoring status changed: {previous} -> {monitoring_status} "
            f"({crossing.crossing_code})"
        ),
    )
    return crossing


def activate_crossing(
    db: Session,
    crossing_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayCrossing:
    crossing = require_entity(
        get_crossing_by_id(db, crossing_id), name="Railway crossing"
    )
    assert isinstance(crossing, RailwayCrossing)
    crossing.is_active = True
    crossing.status = "active"
    crossing.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(crossing)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_CROSSING_ACTIVATED,
        entity_type="railway_crossing",
        entity_id=str(crossing.id),
        details=f"Crossing activated: {crossing.crossing_code}",
    )
    return crossing


def deactivate_crossing(
    db: Session,
    crossing_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayCrossing:
    crossing = require_entity(
        get_crossing_by_id(db, crossing_id), name="Railway crossing"
    )
    assert isinstance(crossing, RailwayCrossing)
    crossing.is_active = False
    crossing.status = "inactive"
    crossing.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(crossing)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_CROSSING_DEACTIVATED,
        entity_type="railway_crossing",
        entity_id=str(crossing.id),
        details=f"Crossing deactivated: {crossing.crossing_code}",
    )
    return crossing
