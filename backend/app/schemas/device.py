"""Device Pydantic schemas."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    device_code: str = Field(min_length=1, max_length=100)
    device_name: str = Field(min_length=1, max_length=255)
    device_type: str = Field(min_length=1, max_length=100)
    serial_number: Optional[str] = Field(default=None, max_length=100)
    manufacturer: Optional[str] = Field(default=None, max_length=100)
    model_name: Optional[str] = Field(default=None, max_length=100)
    hardware_version: Optional[str] = Field(default=None, max_length=50)
    firmware_version: Optional[str] = Field(default=None, max_length=50)
    crossing_id: Optional[int] = None
    installation_location: Optional[str] = Field(default=None, max_length=255)
    mac_address: Optional[str] = Field(default=None, max_length=50)
    ip_address: Optional[str] = Field(default=None, max_length=50)
    communication_type: str = Field(default="SIMULATED")
    configuration: Optional[dict[str, Any]] = None
    metadata_json: Optional[dict[str, Any]] = None


class DeviceUpdate(BaseModel):
    device_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    device_type: Optional[str] = None
    serial_number: Optional[str] = Field(default=None, max_length=100)
    manufacturer: Optional[str] = Field(default=None, max_length=100)
    model_name: Optional[str] = Field(default=None, max_length=100)
    hardware_version: Optional[str] = Field(default=None, max_length=50)
    firmware_version: Optional[str] = Field(default=None, max_length=50)
    installation_location: Optional[str] = Field(default=None, max_length=255)
    mac_address: Optional[str] = Field(default=None, max_length=50)
    ip_address: Optional[str] = Field(default=None, max_length=50)
    communication_type: Optional[str] = None
    configuration: Optional[dict[str, Any]] = None
    metadata_json: Optional[dict[str, Any]] = None


class DeviceAssignmentRequest(BaseModel):
    crossing_id: int


class DeviceStatusUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=50)


class DeviceHealthStatusUpdate(BaseModel):
    health_status: str = Field(min_length=1, max_length=50)


class DeviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_code: str
    device_name: str
    device_type: str
    serial_number: Optional[str] = None
    manufacturer: Optional[str] = None
    model_name: Optional[str] = None
    hardware_version: Optional[str] = None
    firmware_version: Optional[str] = None
    crossing_id: Optional[int] = None
    location: Optional[str] = None
    installation_location: Optional[str] = None
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    communication_type: str
    status: str
    health_status: str
    last_seen_at: Optional[datetime] = None
    registered_at: Optional[datetime] = None
    activated_at: Optional[datetime] = None
    deactivated_at: Optional[datetime] = None
    is_active: bool
    configuration: Optional[dict[str, Any]] = None
    metadata_json: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None


DeviceListItem = DeviceResponse
