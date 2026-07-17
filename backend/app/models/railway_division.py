"""Railway division organizational model."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.railway_station import RailwayStation
    from app.models.railway_zone import RailwayZone
    from app.models.staff_assignment import StaffAssignment

STATUS_ACTIVE = "ACTIVE"
STATUS_INACTIVE = "INACTIVE"
STATUS_MAINTENANCE = "MAINTENANCE"
STATUS_ARCHIVED = "ARCHIVED"

VALID_DIVISION_STATUSES = (
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    STATUS_MAINTENANCE,
    STATUS_ARCHIVED,
)


class RailwayDivision(Base):
    __tablename__ = "railway_divisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    division_code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    division_name: Mapped[str] = mapped_column(String(255), nullable=False)
    zone_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("railway_zones.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    headquarters: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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

    zone: Mapped["RailwayZone"] = relationship(
        "RailwayZone",
        back_populates="divisions",
        foreign_keys=[zone_id],
    )
    stations: Mapped[list["RailwayStation"]] = relationship(
        "RailwayStation",
        back_populates="division",
        foreign_keys="RailwayStation.division_id",
    )
    staff_assignments: Mapped[list["StaffAssignment"]] = relationship(
        "StaffAssignment",
        back_populates="division",
        foreign_keys="StaffAssignment.division_id",
    )
