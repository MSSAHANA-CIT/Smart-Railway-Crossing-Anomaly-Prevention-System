"""Sensor Pydantic schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class SensorCreate(BaseModel):
    sensor_code: str = Field(min_length=1, max_length=100)
    sensor_name: str = Field(min_length=1, max_length=255)
    sensor_type_id: int
    device_id: int
    crossing_id: Optional[int] = None
    manufacturer: Optional[str] = Field(default=None, max_length=100)
    model_name: Optional[str] = Field(default=None, max_length=100)
    unit: Optional[str] = Field(default=None, max_length=50)
    measurement_type: Optional[str] = Field(default=None, max_length=100)
    minimum_value: Optional[Decimal] = None
    maximum_value: Optional[Decimal] = None
    warning_threshold: Optional[Decimal] = None
    critical_threshold: Optional[Decimal] = None
    installation_position: Optional[str] = Field(default=None, max_length=255)
    gpio_reference: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Provisional GPIO label only — not a verified hardware mapping",
    )
    calibration_required: bool = False
    configuration: Optional[dict[str, Any]] = None
    metadata_json: Optional[dict[str, Any]] = None


class SensorUpdate(BaseModel):
    sensor_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    manufacturer: Optional[str] = Field(default=None, max_length=100)
    model_name: Optional[str] = Field(default=None, max_length=100)
    unit: Optional[str] = Field(default=None, max_length=50)
    measurement_type: Optional[str] = Field(default=None, max_length=100)
    minimum_value: Optional[Decimal] = None
    maximum_value: Optional[Decimal] = None
    warning_threshold: Optional[Decimal] = None
    critical_threshold: Optional[Decimal] = None
    installation_position: Optional[str] = Field(default=None, max_length=255)
    gpio_reference: Optional[str] = Field(default=None, max_length=100)
    calibration_required: Optional[bool] = None
    configuration: Optional[dict[str, Any]] = None
    metadata_json: Optional[dict[str, Any]] = None


class SensorStatusUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=50)


class SensorHealthStatusUpdate(BaseModel):
    health_status: str = Field(min_length=1, max_length=50)


class SensorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_code: str
    sensor_name: str
    sensor_type_id: int
    device_id: int
    crossing_id: Optional[int] = None
    manufacturer: Optional[str] = None
    model_name: Optional[str] = None
    unit: Optional[str] = None
    measurement_type: Optional[str] = None
    minimum_value: Optional[Decimal] = None
    maximum_value: Optional[Decimal] = None
    warning_threshold: Optional[Decimal] = None
    critical_threshold: Optional[Decimal] = None
    status: str
    health_status: str
    installation_position: Optional[str] = None
    gpio_reference: Optional[str] = None
    calibration_required: bool
    last_calibrated_at: Optional[datetime] = None
    last_seen_at: Optional[datetime] = None
    is_active: bool
    configuration: Optional[dict[str, Any]] = None
    metadata_json: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None


SensorListItem = SensorResponse
