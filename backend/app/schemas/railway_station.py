"""Railway station Pydantic schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RailwayStationCreate(BaseModel):
    station_code: str = Field(min_length=1, max_length=50)
    station_name: str = Field(min_length=1, max_length=255)
    division_id: int
    station_type: str = Field(default="STANDARD")
    address: Optional[str] = Field(default=None, max_length=500)
    city: Optional[str] = Field(default=None, max_length=100)
    district: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    postal_code: Optional[str] = Field(default=None, max_length=20)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    contact_phone: Optional[str] = Field(default=None, max_length=50)
    status: str = Field(default="ACTIVE")


class RailwayStationUpdate(BaseModel):
    station_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    division_id: Optional[int] = None
    station_type: Optional[str] = None
    address: Optional[str] = Field(default=None, max_length=500)
    city: Optional[str] = Field(default=None, max_length=100)
    district: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    postal_code: Optional[str] = Field(default=None, max_length=20)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    contact_phone: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = None


class RailwayStationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    station_code: str
    station_name: str
    division_id: int
    station_type: str
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    contact_phone: Optional[str] = None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None


RailwayStationListItem = RailwayStationResponse
