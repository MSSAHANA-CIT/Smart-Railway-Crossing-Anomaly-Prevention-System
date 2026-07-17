"""Railway zone organizational model."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.railway_division import RailwayDivision
    from app.models.staff_assignment import StaffAssignment

STATUS_ACTIVE = "ACTIVE"
STATUS_INACTIVE = "INACTIVE"
STATUS_MAINTENANCE = "MAINTENANCE"
STATUS_ARCHIVED = "ARCHIVED"

VALID_ZONE_STATUSES = (
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    STATUS_MAINTENANCE,
    STATUS_ARCHIVED,
)


class RailwayZone(Base):
    __tablename__ = "railway_zones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    zone_code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    zone_name: Mapped[str] = mapped_column(String(255), nullable=False)
    headquarters: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    state_coverage: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
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

    divisions: Mapped[list["RailwayDivision"]] = relationship(
        "RailwayDivision",
        back_populates="zone",
        foreign_keys="RailwayDivision.zone_id",
    )
    staff_assignments: Mapped[list["StaffAssignment"]] = relationship(
        "StaffAssignment",
        back_populates="zone",
        foreign_keys="StaffAssignment.zone_id",
    )
