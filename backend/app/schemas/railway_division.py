"""Railway division Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RailwayDivisionCreate(BaseModel):
    division_code: str = Field(min_length=1, max_length=50)
    division_name: str = Field(min_length=1, max_length=255)
    zone_id: int
    headquarters: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    status: str = Field(default="ACTIVE")


class RailwayDivisionUpdate(BaseModel):
    division_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    zone_id: Optional[int] = None
    headquarters: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None


class RailwayDivisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    division_code: str
    division_name: str
    zone_id: int
    headquarters: Optional[str] = None
    description: Optional[str] = None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None


RailwayDivisionListItem = RailwayDivisionResponse
