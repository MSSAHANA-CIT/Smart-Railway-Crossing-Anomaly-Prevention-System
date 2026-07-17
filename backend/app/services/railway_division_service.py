"""Railway division service."""

from typing import Optional

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.railway_division import (
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    VALID_DIVISION_STATUSES,
    RailwayDivision,
)
from app.schemas.railway_division import RailwayDivisionCreate, RailwayDivisionUpdate
from app.services.audit_service import (
    RAILWAY_DIVISION_ACTIVATED,
    RAILWAY_DIVISION_CREATED,
    RAILWAY_DIVISION_DEACTIVATED,
    RAILWAY_DIVISION_UPDATED,
    create_audit_log,
)
from app.services.railway_zone_service import get_zone_by_id
from app.utils.validation import conflict, require_entity, require_valid_choice


def get_division_by_id(db: Session, division_id: int) -> Optional[RailwayDivision]:
    return db.get(RailwayDivision, division_id)


def get_division_by_code(db: Session, division_code: str) -> Optional[RailwayDivision]:
    return db.scalar(
        select(RailwayDivision).where(RailwayDivision.division_code == division_code)
    )


def list_divisions(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    zone_id: Optional[int] = None,
    status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
) -> tuple[list[RailwayDivision], int]:
    stmt = select(RailwayDivision)
    count_stmt = select(func.count()).select_from(RailwayDivision)

    if zone_id is not None:
        stmt = stmt.where(RailwayDivision.zone_id == zone_id)
        count_stmt = count_stmt.where(RailwayDivision.zone_id == zone_id)
    if status is not None:
        stmt = stmt.where(RailwayDivision.status == status)
        count_stmt = count_stmt.where(RailwayDivision.status == status)
    if is_active is not None:
        stmt = stmt.where(RailwayDivision.is_active.is_(is_active))
        count_stmt = count_stmt.where(RailwayDivision.is_active.is_(is_active))
    if search:
        pattern = f"%{search}%"
        search_filter = or_(
            RailwayDivision.division_code.ilike(pattern),
            RailwayDivision.division_name.ilike(pattern),
            RailwayDivision.headquarters.ilike(pattern),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    total = db.scalar(count_stmt) or 0
    items = list(
        db.scalars(
            stmt.order_by(RailwayDivision.division_code.asc()).offset(skip).limit(limit)
        )
    )
    return items, total


def create_division(
    db: Session,
    data: RailwayDivisionCreate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayDivision:
    require_valid_choice(data.status, VALID_DIVISION_STATUSES, field_name="status")
    require_entity(get_zone_by_id(db, data.zone_id), name="Parent railway zone")
    if get_division_by_code(db, data.division_code):
        raise conflict(f"Division code '{data.division_code}' already exists.")

    division = RailwayDivision(
        division_code=data.division_code.strip().upper(),
        division_name=data.division_name.strip(),
        zone_id=data.zone_id,
        headquarters=data.headquarters,
        description=data.description,
        status=data.status,
        is_active=True,
        created_by_user_id=actor_user_id,
        updated_by_user_id=actor_user_id,
    )
    db.add(division)
    db.commit()
    db.refresh(division)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_DIVISION_CREATED,
        entity_type="railway_division",
        entity_id=str(division.id),
        details=f"Division created: {division.division_code} zone_id={division.zone_id}",
    )
    return division


def update_division(
    db: Session,
    division_id: int,
    data: RailwayDivisionUpdate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayDivision:
    division = require_entity(
        get_division_by_id(db, division_id), name="Railway division"
    )
    assert isinstance(division, RailwayDivision)

    payload = data.model_dump(exclude_unset=True)
    if "status" in payload and payload["status"] is not None:
        require_valid_choice(
            payload["status"], VALID_DIVISION_STATUSES, field_name="status"
        )
    if "zone_id" in payload and payload["zone_id"] is not None:
        require_entity(
            get_zone_by_id(db, payload["zone_id"]), name="Parent railway zone"
        )

    for field, value in payload.items():
        setattr(division, field, value)
    division.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(division)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_DIVISION_UPDATED,
        entity_type="railway_division",
        entity_id=str(division.id),
        details=f"Division updated: {division.division_code}",
    )
    return division


def activate_division(
    db: Session,
    division_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayDivision:
    division = require_entity(
        get_division_by_id(db, division_id), name="Railway division"
    )
    assert isinstance(division, RailwayDivision)
    division.is_active = True
    division.status = STATUS_ACTIVE
    division.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(division)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_DIVISION_ACTIVATED,
        entity_type="railway_division",
        entity_id=str(division.id),
        details=f"Division activated: {division.division_code}",
    )
    return division


def deactivate_division(
    db: Session,
    division_id: int,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> RailwayDivision:
    division = require_entity(
        get_division_by_id(db, division_id), name="Railway division"
    )
    assert isinstance(division, RailwayDivision)
    division.is_active = False
    division.status = STATUS_INACTIVE
    division.updated_by_user_id = actor_user_id
    db.commit()
    db.refresh(division)
    create_audit_log(
        db,
        actor=actor,
        action=RAILWAY_DIVISION_DEACTIVATED,
        entity_type="railway_division",
        entity_id=str(division.id),
        details=f"Division deactivated: {division.division_code}",
    )
    return division
