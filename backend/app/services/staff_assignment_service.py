"""Staff assignment service."""

from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.models.staff_assignment import (
    ASSIGNMENT_TYPE_CROSSING,
    ASSIGNMENT_TYPE_DEVICE,
    ASSIGNMENT_TYPE_DIVISION,
    ASSIGNMENT_TYPE_STATION,
    ASSIGNMENT_TYPE_ZONE,
    VALID_ASSIGNMENT_TYPES,
    StaffAssignment,
)
from app.schemas.staff_assignment import StaffAssignmentCreate, StaffAssignmentUpdate
from app.services.audit_service import (
    STAFF_ASSIGNMENT_ACTIVATED,
    STAFF_ASSIGNMENT_CREATED,
    STAFF_ASSIGNMENT_DEACTIVATED,
    STAFF_ASSIGNMENT_UPDATED,
    create_audit_log,
)
from app.services.device_service import get_device_by_id
from app.services.railway_crossing_service import get_crossing_by_id
from app.services.railway_division_service import get_division_by_id
from app.services.railway_station_service import get_station_by_id
from app.services.railway_zone_service import get_zone_by_id
from app.services.user_service import get_user_by_id
from app.utils.validation import bad_request, conflict, require_entity, require_valid_choice


RESOURCE_FIELD_BY_TYPE = {
    ASSIGNMENT_TYPE_ZONE: "zone_id",
    ASSIGNMENT_TYPE_DIVISION: "division_id",
    ASSIGNMENT_TYPE_STATION: "station_id",
    ASSIGNMENT_TYPE_CROSSING: "crossing_id",
    ASSIGNMENT_TYPE_DEVICE: "device_id",
}


def get_assignment_by_id(
    db: Session, assignment_id: int
) -> Optional[StaffAssignment]:
    return db.get(StaffAssignment, assignment_id)


def _validate_assignment_resources(
    db: Session, data: StaffAssignmentCreate
) -> dict[str, Optional[int]]:
    require_valid_choice(
        data.assignment_type, VALID_ASSIGNMENT_TYPES, field_name="assignment_type"
    )
    require_entity(get_user_by_id(db, data.user_id), name="User")

    required_field = RESOURCE_FIELD_BY_TYPE[data.assignment_type]
    resource_values = {
        "zone_id": data.zone_id,
        "division_id": data.division_id,
        "station_id": data.station_id,
        "crossing_id": data.crossing_id,
        "device_id": data.device_id,
    }

    if resource_values[required_field] is None:
        raise bad_request(
            f"assignment_type {data.assignment_type} requires {required_field}."
        )

    # Clear unrelated resource FKs for consistency
    cleaned = {key: None for key in resource_values}
    cleaned[required_field] = resource_values[required_field]

    resource_id = cleaned[required_field]
    assert resource_id is not None

    if data.assignment_type == ASSIGNMENT_TYPE_ZONE:
        require_entity(get_zone_by_id(db, resource_id), name="Railway zone")
    elif data.assignment_type == ASSIGNMENT_TYPE_DIVISION:
        require_entity(get_division_by_id(db, resource_id), name="Railway division")
    elif data.assignment_type == ASSIGNMENT_TYPE_STATION:
        require_entity(get_station_by_id(db, resource_id), name="Railway station")
    elif data.assignment_type == ASSIGNMENT_TYPE_CROSSING:
        require_entity(get_crossing_by_id(db, resource_id), name="Railway crossing")
    elif data.assignment_type == ASSIGNMENT_TYPE_DEVICE:
        require_entity(get_device_by_id(db, resource_id), name="Device")

    return cleaned


def _find_duplicate_active(
    db: Session,
    *,
    user_id: int,
    assignment_type: str,
    zone_id: Optional[int],
    division_id: Optional[int],
    station_id: Optional[int],
    crossing_id: Optional[int],
    device_id: Optional[int],
    exclude_id: Optional[int] = None,
) -> Optional[StaffAssignment]:
    stmt = select(StaffAssignment).where(
        and_(
            StaffAssignment.user_id == user_id,
            StaffAssignment.assignment_type == assignment_type,
            StaffAssignment.is_active.is_(True),
            StaffAssignment.zone_id == zone_id,
            StaffAssignment.division_id == division_id,
            StaffAssignment.station_id == station_id,
            StaffAssignment.crossing_id == crossing_id,
            StaffAssignment.device_id == device_id,
        )
    )
    if exclude_id is not None:
        stmt = stmt.where(StaffAssignment.id != exclude_id)
    return db.scalar(stmt)


def list_assignments(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    user_id: Optional[int] = None,
    assignment_type: Optional[str] = None,
    zone_id: Optional[int] = None,
    division_id: Optional[int] = None,
    station_id: Optional[int] = None,
    crossing_id: Optional[int] = None,
    device_id: Optional[int] = None,
    is_active: Optional[bool] = None,
) -> tuple[list[StaffAssignment], int]:
    stmt = select(StaffAssignment)
    count_stmt = select(func.count()).select_from(StaffAssignment)

    filters = {
        "user_id": user_id,
        "assignment_type": assignment_type,
        "zone_id": zone_id,
        "division_id": division_id,
        "station_id": station_id,
        "crossing_id": crossing_id,
        "device_id": device_id,
    }
    for attr, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(StaffAssignment, attr) == value)
            count_stmt = count_stmt.where(getattr(StaffAssignment, attr) == value)

    if is_active is not None:
        stmt = stmt.where(StaffAssignment.is_active.is_(is_active))
        count_stmt = count_stmt.where(StaffAssignment.is_active.is_(is_active))

    total = db.scalar(count_stmt) or 0
    items = list(
        db.scalars(
            stmt.order_by(StaffAssignment.created_at.desc()).offset(skip).limit(limit)
        )
    )
    return items, total


def create_assignment(
    db: Session,
    data: StaffAssignmentCreate,
    *,
    actor: str,
    actor_user_id: Optional[int] = None,
) -> StaffAssignment:
    resources = _validate_assignment_resources(db, data)
    duplicate = _find_duplicate_active(
        db,
        user_id=data.user_id,
        assignment_type=data.assignment_type,
        zone_id=resources["zone_id"],
        division_id=resources["division_id"],
        station_id=resources["station_id"],
        crossing_id=resources["crossing_id"],
        device_id=resources["device_id"],
    )
    if duplicate:
        raise conflict(
            "An identical active staff assignment already exists for this user and resource."
        )

    assignment = StaffAssignment(
        user_id=data.user_id,
        assignment_type=data.assignment_type,
        zone_id=resources["zone_id"],
        division_id=resources["division_id"],
        station_id=resources["station_id"],
        crossing_id=resources["crossing_id"],
        device_id=resources["device_id"],
        responsibility=data.responsibility,
        shift_name=data.shift_name,
        start_date=data.start_date,
        end_date=data.end_date,
        is_primary=data.is_primary,
        is_active=True,
        assigned_by_user_id=actor_user_id,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    create_audit_log(
        db,
        actor=actor,
        action=STAFF_ASSIGNMENT_CREATED,
        entity_type="staff_assignment",
        entity_id=str(assignment.id),
        details=(
            f"Assignment created: user_id={assignment.user_id} "
            f"type={assignment.assignment_type}"
        ),
    )
    return assignment


def update_assignment(
    db: Session,
    assignment_id: int,
    data: StaffAssignmentUpdate,
    *,
    actor: str,
) -> StaffAssignment:
    assignment = require_entity(
        get_assignment_by_id(db, assignment_id), name="Staff assignment"
    )
    assert isinstance(assignment, StaffAssignment)

    payload = data.model_dump(exclude_unset=True)
    for field, value in payload.items():
        setattr(assignment, field, value)
    db.commit()
    db.refresh(assignment)
    create_audit_log(
        db,
        actor=actor,
        action=STAFF_ASSIGNMENT_UPDATED,
        entity_type="staff_assignment",
        entity_id=str(assignment.id),
        details=f"Assignment updated: id={assignment.id}",
    )
    return assignment


def activate_assignment(
    db: Session,
    assignment_id: int,
    *,
    actor: str,
) -> StaffAssignment:
    assignment = require_entity(
        get_assignment_by_id(db, assignment_id), name="Staff assignment"
    )
    assert isinstance(assignment, StaffAssignment)

    duplicate = _find_duplicate_active(
        db,
        user_id=assignment.user_id,
        assignment_type=assignment.assignment_type,
        zone_id=assignment.zone_id,
        division_id=assignment.division_id,
        station_id=assignment.station_id,
        crossing_id=assignment.crossing_id,
        device_id=assignment.device_id,
        exclude_id=assignment.id,
    )
    if duplicate:
        raise conflict(
            "Cannot activate: an identical active assignment already exists."
        )

    assignment.is_active = True
    db.commit()
    db.refresh(assignment)
    create_audit_log(
        db,
        actor=actor,
        action=STAFF_ASSIGNMENT_ACTIVATED,
        entity_type="staff_assignment",
        entity_id=str(assignment.id),
        details=f"Assignment activated: id={assignment.id}",
    )
    return assignment


def deactivate_assignment(
    db: Session,
    assignment_id: int,
    *,
    actor: str,
) -> StaffAssignment:
    assignment = require_entity(
        get_assignment_by_id(db, assignment_id), name="Staff assignment"
    )
    assert isinstance(assignment, StaffAssignment)
    assignment.is_active = False
    db.commit()
    db.refresh(assignment)
    create_audit_log(
        db,
        actor=actor,
        action=STAFF_ASSIGNMENT_DEACTIVATED,
        entity_type="staff_assignment",
        entity_id=str(assignment.id),
        details=f"Assignment deactivated: id={assignment.id}",
    )
    return assignment
