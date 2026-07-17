"""Railway crossing model — expands Phase S2 crossings table."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.device import Device
    from app.models.railway_division import RailwayDivision
    from app.models.railway_station import RailwayStation
    from app.models.railway_zone import RailwayZone
    from app.models.sensor import Sensor
    from app.models.staff_assignment import StaffAssignment

CROSSING_TYPE_MANNED = "MANNED"
CROSSING_TYPE_UNMANNED = "UNMANNED"
CROSSING_TYPE_ROAD_UNDER_BRIDGE = "ROAD_UNDER_BRIDGE"
CROSSING_TYPE_ROAD_OVER_BRIDGE = "ROAD_OVER_BRIDGE"
CROSSING_TYPE_PEDESTRIAN = "PEDESTRIAN"
CROSSING_TYPE_PRIVATE = "PRIVATE"
CROSSING_TYPE_OTHER = "OTHER"

VALID_CROSSING_TYPES = (
    CROSSING_TYPE_MANNED,
    CROSSING_TYPE_UNMANNED,
    CROSSING_TYPE_ROAD_UNDER_BRIDGE,
    CROSSING_TYPE_ROAD_OVER_BRIDGE,
    CROSSING_TYPE_PEDESTRIAN,
    CROSSING_TYPE_PRIVATE,
    CROSSING_TYPE_OTHER,
)

GATE_TYPE_FULL_BARRIER = "FULL_BARRIER"
GATE_TYPE_HALF_BARRIER = "HALF_BARRIER"
GATE_TYPE_MANUAL = "MANUAL"
GATE_TYPE_AUTOMATIC = "AUTOMATIC"
GATE_TYPE_NO_GATE = "NO_GATE"
GATE_TYPE_PROTOTYPE = "PROTOTYPE"

VALID_GATE_TYPES = (
    GATE_TYPE_FULL_BARRIER,
    GATE_TYPE_HALF_BARRIER,
    GATE_TYPE_MANUAL,
    GATE_TYPE_AUTOMATIC,
    GATE_TYPE_NO_GATE,
    GATE_TYPE_PROTOTYPE,
)

RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_CRITICAL = "CRITICAL"
RISK_NOT_ASSESSED = "NOT_ASSESSED"

VALID_RISK_CATEGORIES = (
    RISK_LOW,
    RISK_MEDIUM,
    RISK_HIGH,
    RISK_CRITICAL,
    RISK_NOT_ASSESSED,
)

OP_STATUS_OPERATIONAL = "OPERATIONAL"
OP_STATUS_MAINTENANCE = "MAINTENANCE"
OP_STATUS_TEMPORARILY_CLOSED = "TEMPORARILY_CLOSED"
OP_STATUS_DECOMMISSIONED = "DECOMMISSIONED"
OP_STATUS_TESTING = "TESTING"

VALID_OPERATIONAL_STATUSES = (
    OP_STATUS_OPERATIONAL,
    OP_STATUS_MAINTENANCE,
    OP_STATUS_TEMPORARILY_CLOSED,
    OP_STATUS_DECOMMISSIONED,
    OP_STATUS_TESTING,
)

MON_STATUS_NOT_CONFIGURED = "NOT_CONFIGURED"
MON_STATUS_OFFLINE = "OFFLINE"
MON_STATUS_ONLINE = "ONLINE"
MON_STATUS_WARNING = "WARNING"
MON_STATUS_CRITICAL = "CRITICAL"

VALID_MONITORING_STATUSES = (
    MON_STATUS_NOT_CONFIGURED,
    MON_STATUS_OFFLINE,
    MON_STATUS_ONLINE,
    MON_STATUS_WARNING,
    MON_STATUS_CRITICAL,
)


class RailwayCrossing(Base):
    """
    Railway crossing entity.

    Table name remains ``crossings`` from Phase S2 for backward compatibility.
    Legacy columns (location, zone, state, country, status) are retained.
    """

    __tablename__ = "crossings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crossing_code: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    crossing_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Legacy Phase S2 fields (preserved)
    location: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    zone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="India")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")

    # Phase S4 hierarchy FKs
    station_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("railway_stations.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    division_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("railway_divisions.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    zone_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("railway_zones.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    crossing_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=CROSSING_TYPE_OTHER
    )
    road_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    landmark: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    gate_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=GATE_TYPE_PROTOTYPE
    )
    number_of_tracks: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    risk_category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=RISK_NOT_ASSESSED,
        index=True,
    )
    operational_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=OP_STATUS_TESTING,
        index=True,
    )
    monitoring_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=MON_STATUS_NOT_CONFIGURED,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_by_user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    updated_by_user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    station: Mapped[Optional["RailwayStation"]] = relationship(
        "RailwayStation",
        back_populates="crossings",
        foreign_keys=[station_id],
    )
    division: Mapped[Optional["RailwayDivision"]] = relationship(
        "RailwayDivision",
        foreign_keys=[division_id],
    )
    parent_zone: Mapped[Optional["RailwayZone"]] = relationship(
        "RailwayZone",
        foreign_keys=[zone_id],
    )
    devices: Mapped[list["Device"]] = relationship(
        "Device",
        back_populates="crossing",
        foreign_keys="Device.crossing_id",
    )
    sensors: Mapped[list["Sensor"]] = relationship(
        "Sensor",
        back_populates="crossing",
        foreign_keys="Sensor.crossing_id",
    )
    staff_assignments: Mapped[list["StaffAssignment"]] = relationship(
        "StaffAssignment",
        back_populates="crossing",
        foreign_keys="StaffAssignment.crossing_id",
    )


# Backward-compatible alias used by Phase S2 imports
Crossing = RailwayCrossing
