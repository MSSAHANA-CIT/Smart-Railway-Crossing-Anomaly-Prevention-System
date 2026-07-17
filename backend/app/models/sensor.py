"""Sensor model for sensors registered under devices."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Optional

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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.device import Device
    from app.models.railway_crossing import RailwayCrossing
    from app.models.sensor_type import SensorType

SENSOR_STATUS_REGISTERED = "REGISTERED"
SENSOR_STATUS_PENDING_INSTALLATION = "PENDING_INSTALLATION"
SENSOR_STATUS_INSTALLED = "INSTALLED"
SENSOR_STATUS_ACTIVE = "ACTIVE"
SENSOR_STATUS_INACTIVE = "INACTIVE"
SENSOR_STATUS_MAINTENANCE = "MAINTENANCE"
SENSOR_STATUS_DISABLED = "DISABLED"

VALID_SENSOR_STATUSES = (
    SENSOR_STATUS_REGISTERED,
    SENSOR_STATUS_PENDING_INSTALLATION,
    SENSOR_STATUS_INSTALLED,
    SENSOR_STATUS_ACTIVE,
    SENSOR_STATUS_INACTIVE,
    SENSOR_STATUS_MAINTENANCE,
    SENSOR_STATUS_DISABLED,
)

HEALTH_UNKNOWN = "UNKNOWN"
HEALTH_HEALTHY = "HEALTHY"
HEALTH_WARNING = "WARNING"
HEALTH_CRITICAL = "CRITICAL"
HEALTH_OFFLINE = "OFFLINE"

VALID_SENSOR_HEALTH_STATUSES = (
    HEALTH_UNKNOWN,
    HEALTH_HEALTHY,
    HEALTH_WARNING,
    HEALTH_CRITICAL,
    HEALTH_OFFLINE,
)


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_code: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    sensor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sensor_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sensor_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("devices.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    crossing_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("crossings.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    manufacturer: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    measurement_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    minimum_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 6), nullable=True)
    maximum_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 6), nullable=True)
    warning_threshold: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 6), nullable=True
    )
    critical_threshold: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 6), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=SENSOR_STATUS_REGISTERED,
        index=True,
    )
    health_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=HEALTH_UNKNOWN,
        index=True,
    )
    installation_position: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    gpio_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    calibration_required: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    last_calibrated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    configuration: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    metadata_json: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
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

    sensor_type: Mapped["SensorType"] = relationship(
        "SensorType",
        foreign_keys=[sensor_type_id],
    )
    device: Mapped["Device"] = relationship(
        "Device",
        back_populates="sensors",
        foreign_keys=[device_id],
    )
    crossing: Mapped[Optional["RailwayCrossing"]] = relationship(
        "RailwayCrossing",
        back_populates="sensors",
        foreign_keys=[crossing_id],
    )
