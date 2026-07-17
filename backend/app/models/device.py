"""Device model for field hardware (ESP32 controllers, cameras, etc.)."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.railway_crossing import RailwayCrossing
    from app.models.sensor import Sensor
    from app.models.staff_assignment import StaffAssignment

DEVICE_TYPE_ESP32_SENSOR_CONTROLLER = "ESP32_SENSOR_CONTROLLER"
DEVICE_TYPE_ESP32S3_AI_CAMERA = "ESP32S3_AI_CAMERA"
DEVICE_TYPE_GATE_CONTROLLER = "GATE_CONTROLLER"
DEVICE_TYPE_CAMERA_CONTROLLER = "CAMERA_CONTROLLER"
DEVICE_TYPE_ENVIRONMENT_MONITOR = "ENVIRONMENT_MONITOR"
DEVICE_TYPE_PROTOTYPE_CONTROLLER = "PROTOTYPE_CONTROLLER"
DEVICE_TYPE_OTHER = "OTHER"

VALID_DEVICE_TYPES = (
    DEVICE_TYPE_ESP32_SENSOR_CONTROLLER,
    DEVICE_TYPE_ESP32S3_AI_CAMERA,
    DEVICE_TYPE_GATE_CONTROLLER,
    DEVICE_TYPE_CAMERA_CONTROLLER,
    DEVICE_TYPE_ENVIRONMENT_MONITOR,
    DEVICE_TYPE_PROTOTYPE_CONTROLLER,
    DEVICE_TYPE_OTHER,
)

COMM_WIFI = "WIFI"
COMM_ETHERNET = "ETHERNET"
COMM_GSM = "GSM"
COMM_LORA = "LORA"
COMM_SERIAL = "SERIAL"
COMM_ESP_NOW = "ESP_NOW"
COMM_SIMULATED = "SIMULATED"
COMM_UNKNOWN = "UNKNOWN"

VALID_COMMUNICATION_TYPES = (
    COMM_WIFI,
    COMM_ETHERNET,
    COMM_GSM,
    COMM_LORA,
    COMM_SERIAL,
    COMM_ESP_NOW,
    COMM_SIMULATED,
    COMM_UNKNOWN,
)

DEVICE_STATUS_REGISTERED = "REGISTERED"
DEVICE_STATUS_PENDING_ACTIVATION = "PENDING_ACTIVATION"
DEVICE_STATUS_ACTIVE = "ACTIVE"
DEVICE_STATUS_INACTIVE = "INACTIVE"
DEVICE_STATUS_MAINTENANCE = "MAINTENANCE"
DEVICE_STATUS_DISABLED = "DISABLED"
DEVICE_STATUS_DECOMMISSIONED = "DECOMMISSIONED"

VALID_DEVICE_STATUSES = (
    DEVICE_STATUS_REGISTERED,
    DEVICE_STATUS_PENDING_ACTIVATION,
    DEVICE_STATUS_ACTIVE,
    DEVICE_STATUS_INACTIVE,
    DEVICE_STATUS_MAINTENANCE,
    DEVICE_STATUS_DISABLED,
    DEVICE_STATUS_DECOMMISSIONED,
)

HEALTH_UNKNOWN = "UNKNOWN"
HEALTH_HEALTHY = "HEALTHY"
HEALTH_WARNING = "WARNING"
HEALTH_CRITICAL = "CRITICAL"
HEALTH_OFFLINE = "OFFLINE"

VALID_HEALTH_STATUSES = (
    HEALTH_UNKNOWN,
    HEALTH_HEALTHY,
    HEALTH_WARNING,
    HEALTH_CRITICAL,
    HEALTH_OFFLINE,
)


class Device(Base):
    __tablename__ = "devices"
    __table_args__ = (
        Index(
            "uq_devices_serial_number",
            "serial_number",
            unique=True,
            postgresql_where=text("serial_number IS NOT NULL"),
        ),
        Index(
            "uq_devices_mac_address",
            "mac_address",
            unique=True,
            postgresql_where=text("mac_address IS NOT NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_code: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    device_name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    serial_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    hardware_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    firmware_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    crossing_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("crossings.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # Legacy Phase S2 field retained
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    installation_location: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    mac_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    communication_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=COMM_UNKNOWN
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=DEVICE_STATUS_REGISTERED,
        index=True,
    )
    health_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=HEALTH_UNKNOWN,
        index=True,
    )
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    registered_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    activated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deactivated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
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

    crossing: Mapped[Optional["RailwayCrossing"]] = relationship(
        "RailwayCrossing",
        back_populates="devices",
        foreign_keys=[crossing_id],
    )
    sensors: Mapped[list["Sensor"]] = relationship(
        "Sensor",
        back_populates="device",
        foreign_keys="Sensor.device_id",
    )
    staff_assignments: Mapped[list["StaffAssignment"]] = relationship(
        "StaffAssignment",
        back_populates="device",
        foreign_keys="StaffAssignment.device_id",
    )
