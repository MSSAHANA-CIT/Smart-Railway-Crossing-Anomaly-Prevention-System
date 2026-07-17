"""Railway station service."""

from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.railway_division import RailwayDivision
from app.models.railway_station import (
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    VALID_STATION_STATUSES,
    VALID_STATION_TYPES,
    RailwayStation,
)
from app.schemas.railway_station import RailwayStationCreate, RailwayStationUpdate
from app.services.audit_service import (
    RAILWAY_STATION_ACTIVATED,
    RAILWAY_STATION_CREATED,
    RAILWAY_STATION_DEACTIVATED,
    RAILWAY_STATION_UPDATED,
    create_audit_log,
)
from app.services.railway_division_service import get_division_by_id
from app.utils.validation import conflict, require_entity, require_valid_choice


def get_station_by_id(db: Session, station_id: int) -> Optional[RailwayStation]:
    return db.get(RailwayStation, station_id)


def get_station_by_code(db: Session, station_code: str) -> Optional[RailwayStation]:
    return db.scalar(
        select(RailwayStation).where(RailwayStation.station_code == station_code)
    )


def list_stations(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    division_id: Optional[int] = None,
    zone_id: Optional[int] = None,
    state: Optional[str] = None,
    station_type: Optional[str] = None,
    status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[list[RailwayStation], int]:
    stmt = select(RailwayStation)
    count_stmt = select(func.count()).select_from(RailwayStation)

    if zone_id is not None:
        stmt = stmt.join(
            RailwayDivision, RailwayStation.division_id == RailwayDivision.id
        ).where(RailwayDivision.zone_id == zone_id)
        count_stmt = count_stmt.join(
            RailwayDivision, RailwayStation.division_id == RailwayDivision.id
        ).where(RailwayDivision.zone_id == zone_id)

    if division_id is not None:
        stmt = stmt.where(RailwayStation.division_id == division_id)
        count_stmt = count_stmt.where(RailwayStation.division_id == division_id)
    if state is not None:
        stmt = stmt.where(RailwayStation.state == state)
        count_stmt = count_stmt.where(RailwayStation.state == state)
    if station_type is not None:
        stmt = stmt.where(RailwayStation.station_type == station_type)
        count_stmt = count_stmt.where(RailwayStation.station_type == station_type)
    if status is not None:
        stmt = stmt.where(RailwayStation.status == status)
        count_stmt = count_stmt.where(RailwayStation.status == status)
    if is_active is not None:
        stmt = stmt.where(RailwayStation.is_active.is_(is_active))
        count_stmt = count_stmt.where(RailwayStation.is_active.is_(is_active))
    if search:
        pattern = f"%{search}%"
        search_filter = or_(
            RailwayStation.station_code.ilike(pattern),
            RailwayStation.station_name.ilike(pattern),
            RailwayStation.city.ilike(pattern),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    total = db.scalar(count_stmt) or 0
    items = list(
        db.scalars(
            stmt.order_by(RailwayStation.station_code.asc()).offset(skip).limit(limit)
        )
    )
    return items, total


def create_station(
    db: Session,
    data: RailwayStationCreate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayStation:
    require_valid_choice(data.status, VALID_STATION_STATUSES, field_name="status")
    require_valid_choice(
        data.station_type, VALID_STATION_TYPES, field_name="station_type"
    )
    require_entity(
        get_division_by_id(db, data.division_id), name="Parent railway division"
    )
    if get_station_by_code(db, data.station_code):
        raise conflict(f"Station code '{data.station_code}' already exists.")

    station = RailwayStation(
        station_code=data.station_code.strip().upper(),
        station_name=data.station_name.strip(),
        division_id=data.division_id,
        station_type=data.station_type,
        address=data.address,
        city=data.city,
        district=data.district,
        state=data.state,
        postal_code=data.postal_code,
        latitude=data.latitude,
        longitude=data.longitude,
        contact_phone=data.contact_phone,
        status=data.status,
        is_active=True,
        created_by_user_id=actor_user_id,
        updated_by_user_id=actor_user_id,
    )
    db.add(station)
    db.commit()
    db.refresh(station)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_STATION_CREATED,
        entity_type="railway_station",
        entity_id=str(station.id),
        details=(
            f"Station created: {station.station_code} "
            f"division_id={station.division_id}"
        ),
    )
    return station


def update_station(
    db: Session,
    station_id: int,
    data: RailwayStationUpdate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayStation:
    station = require_entity(
        get_station_by_id(db, station_id), name="Railway station"
    )
    assert isinstance(station, RailwayStation)

    payload = data.model_dump(exclude_unset=True)
    if "status" in payload and payload["status"] is not None:
        require_valid_choice(
            payload["status"], VALID_STATION_STATUSES, field_name="status"
        )
    if "station_type" in payload and payload["station_type"] is not None:
        require_valid_choice(
            payload["station_type"], VALID_STATION_TYPES, field_name="station_type"
        )
    if "division_id" in payload and payload["division_id"] is not None:
        require_entity(
            get_division_by_id(db, payload["division_id"]),
            name="Parent railway division",
        )

    for field, value in payload.items():
        setattr(station, field, value)
    station.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(station)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_STATION_UPDATED,
        entity_type="railway_station",
        entity_id=str(station.id),
        details=f"Station updated: {station.station_code}",
    )
    return station


def activate_station(
    db: Session,
    station_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayStation:
    station = require_entity(
        get_station_by_id(db, station_id), name="Railway station"
    )
    assert isinstance(station, RailwayStation)
    station.is_active = True
    station.status = STATUS_ACTIVE
    station.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(station)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_STATION_ACTIVATED,
        entity_type="railway_station",
        entity_id=str(station.id),
        details=f"Station activated: {station.station_code}",
    )
    return station


def deactivate_station(
    db: Session,
    station_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayStation:
    station = require_entity(
        get_station_by_id(db, station_id), name="Railway station"
    )
    assert isinstance(station, RailwayStation)
    station.is_active = False
    station.status = STATUS_INACTIVE
    station.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(station)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_STATION_DEACTIVATED,
        entity_type="railway_station",
        entity_id=str(station.id),
        details=f"Station deactivated: {station.station_code}",
    )
    return station
