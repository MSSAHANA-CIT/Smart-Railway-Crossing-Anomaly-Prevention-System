"""Railway zone Pydantic schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.railway_zone import VALID_ZONE_STATUSES


class RailwayZoneCreate(BaseModel):
    zone_code: str = Field(min_length=1, max_length=50)
    zone_name: str = Field(min_length=1, max_length=255)
    headquarters: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    state_coverage: Optional[str] = Field(default=None, max_length=255)
    status: str = Field(default="ACTIVE")

    def validated_status(self) -> str:
        if self.status not in VALID_ZONE_STATUSES:
            raise ValueError(
                f"Invalid status. Must be one of: {', '.join(VALID_ZONE_STATUSES)}"
            )
        return self.status


class RailwayZoneUpdate(BaseModel):
    zone_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    headquarters: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    state_coverage: Optional[str] = Field(default=None, max_length=255)
    status: Optional[str] = None


class RailwayZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    zone_code: str
    zone_name: str
    headquarters: Optional[str] = None
    description: Optional[str] = None
    state_coverage: Optional[str] = None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None


RailwayZoneListItem = RailwayZoneResponse
