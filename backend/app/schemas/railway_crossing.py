"""Railway crossing Pydantic schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RailwayCrossingCreate(BaseModel):
    crossing_code: str = Field(min_length=1, max_length=100)
    crossing_name: str = Field(min_length=1, max_length=255)
    station_id: int
    division_id: int
    zone_id: int
    crossing_type: str = Field(default="OTHER")
    road_name: Optional[str] = Field(default=None, max_length=255)
    landmark: Optional[str] = Field(default=None, max_length=255)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    gate_type: str = Field(default="PROTOTYPE")
    number_of_tracks: Optional[int] = Field(default=None, ge=0)
    risk_category: str = Field(default="NOT_ASSESSED")
    operational_status: str = Field(default="TESTING")
    monitoring_status: str = Field(default="NOT_CONFIGURED")
    description: Optional[str] = None
    location: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Legacy location text; defaults from road_name/landmark if omitted",
    )


class RailwayCrossingUpdate(BaseModel):
    crossing_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    station_id: Optional[int] = None
    division_id: Optional[int] = None
    zone_id: Optional[int] = None
    crossing_type: Optional[str] = None
    road_name: Optional[str] = Field(default=None, max_length=255)
    landmark: Optional[str] = Field(default=None, max_length=255)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    gate_type: Optional[str] = None
    number_of_tracks: Optional[int] = Field(default=None, ge=0)
    risk_category: Optional[str] = None
    operational_status: Optional[str] = None
    monitoring_status: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = Field(default=None, max_length=255)


class OperationalStatusUpdate(BaseModel):
    operational_status: str = Field(min_length=1, max_length=50)


class MonitoringStatusUpdate(BaseModel):
    monitoring_status: str = Field(min_length=1, max_length=50)


class RailwayCrossingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    crossing_code: str
    crossing_name: str
    station_id: Optional[int] = None
    division_id: Optional[int] = None
    zone_id: Optional[int] = None
    crossing_type: str
    road_name: Optional[str] = None
    landmark: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    gate_type: str
    number_of_tracks: Optional[int] = None
    risk_category: str
    operational_status: str
    monitoring_status: str
    description: Optional[str] = None
    location: str
    zone: Optional[str] = None
    state: Optional[str] = None
    country: str
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None


RailwayCrossingListItem = RailwayCrossingResponse
