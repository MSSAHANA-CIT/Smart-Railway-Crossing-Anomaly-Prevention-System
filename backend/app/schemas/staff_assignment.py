"""Staff assignment Pydantic schemas."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StaffAssignmentCreate(BaseModel):
    user_id: int
    assignment_type: str = Field(min_length=1, max_length=50)
    zone_id: Optional[int] = None
    division_id: Optional[int] = None
    station_id: Optional[int] = None
    crossing_id: Optional[int] = None
    device_id: Optional[int] = None
    responsibility: Optional[str] = None
    shift_name: Optional[str] = Field(default=None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_primary: bool = False


class StaffAssignmentUpdate(BaseModel):
    responsibility: Optional[str] = None
    shift_name: Optional[str] = Field(default=None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_primary: Optional[bool] = None


class StaffAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    assignment_type: str
    zone_id: Optional[int] = None
    division_id: Optional[int] = None
    station_id: Optional[int] = None
    crossing_id: Optional[int] = None
    device_id: Optional[int] = None
    responsibility: Optional[str] = None
    shift_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_primary: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    assigned_by_user_id: Optional[int] = None


StaffAssignmentListItem = StaffAssignmentResponse
