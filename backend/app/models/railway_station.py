"""Railway station organizational model."""

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
    from app.models.railway_crossing import RailwayCrossing
    from app.models.railway_division import RailwayDivision
    from app.models.staff_assignment import StaffAssignment

STATION_TYPE_MAJOR = "MAJOR"
STATION_TYPE_STANDARD = "STANDARD"
STATION_TYPE_HALT = "HALT"
STATION_TYPE_JUNCTION = "JUNCTION"
STATION_TYPE_TERMINAL = "TERMINAL"
STATION_TYPE_OTHER = "OTHER"

VALID_STATION_TYPES = (
    STATION_TYPE_MAJOR,
    STATION_TYPE_STANDARD,
    STATION_TYPE_HALT,
    STATION_TYPE_JUNCTION,
    STATION_TYPE_TERMINAL,
    STATION_TYPE_OTHER,
)

STATUS_ACTIVE = "ACTIVE"
STATUS_INACTIVE = "INACTIVE"
STATUS_MAINTENANCE = "MAINTENANCE"
STATUS_ARCHIVED = "ARCHIVED"

VALID_STATION_STATUSES = (
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    STATUS_MAINTENANCE,
    STATUS_ARCHIVED,
)


class RailwayStation(Base):
    __tablename__ = "railway_stations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    station_code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    station_name: Mapped[str] = mapped_column(String(255), nullable=False)
    division_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("railway_divisions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    station_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STATION_TYPE_STANDARD
    )
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STATUS_ACTIVE, index=True
    )
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

    division: Mapped["RailwayDivision"] = relationship(
        "RailwayDivision",
        back_populates="stations",
        foreign_keys=[division_id],
    )
    crossings: Mapped[list["RailwayCrossing"]] = relationship(
        "RailwayCrossing",
        back_populates="station",
        foreign_keys="RailwayCrossing.station_id",
    )
    staff_assignments: Mapped[list["StaffAssignment"]] = relationship(
        "StaffAssignment",
        back_populates="station",
        foreign_keys="StaffAssignment.station_id",
    )
