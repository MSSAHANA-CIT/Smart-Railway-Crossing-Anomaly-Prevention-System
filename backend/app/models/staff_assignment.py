"""Staff assignment linking users to organizational resources."""

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.device import Device
    from app.models.railway_crossing import RailwayCrossing
    from app.models.railway_division import RailwayDivision
    from app.models.railway_station import RailwayStation
    from app.models.railway_zone import RailwayZone
    from app.models.user import User

ASSIGNMENT_TYPE_ZONE = "ZONE"
ASSIGNMENT_TYPE_DIVISION = "DIVISION"
ASSIGNMENT_TYPE_STATION = "STATION"
ASSIGNMENT_TYPE_CROSSING = "CROSSING"
ASSIGNMENT_TYPE_DEVICE = "DEVICE"

VALID_ASSIGNMENT_TYPES = (
    ASSIGNMENT_TYPE_ZONE,
    ASSIGNMENT_TYPE_DIVISION,
    ASSIGNMENT_TYPE_STATION,
    ASSIGNMENT_TYPE_CROSSING,
    ASSIGNMENT_TYPE_DEVICE,
)


class StaffAssignment(Base):
    __tablename__ = "staff_assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    assignment_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    zone_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("railway_zones.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    division_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("railway_divisions.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    station_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("railway_stations.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    crossing_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("crossings.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    device_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("devices.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    responsibility: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    shift_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    assigned_by_user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )
    assigned_by: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[assigned_by_user_id],
    )
    zone: Mapped[Optional["RailwayZone"]] = relationship(
        "RailwayZone",
        back_populates="staff_assignments",
        foreign_keys=[zone_id],
    )
    division: Mapped[Optional["RailwayDivision"]] = relationship(
        "RailwayDivision",
        back_populates="staff_assignments",
        foreign_keys=[division_id],
    )
    station: Mapped[Optional["RailwayStation"]] = relationship(
        "RailwayStation",
        back_populates="staff_assignments",
        foreign_keys=[station_id],
    )
    crossing: Mapped[Optional["RailwayCrossing"]] = relationship(
        "RailwayCrossing",
        back_populates="staff_assignments",
        foreign_keys=[crossing_id],
    )
    device: Mapped[Optional["Device"]] = relationship(
        "Device",
        back_populates="staff_assignments",
        foreign_keys=[device_id],
    )
