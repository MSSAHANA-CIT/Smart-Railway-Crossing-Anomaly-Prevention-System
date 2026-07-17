"""Organization hierarchy and overview schemas."""

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.device import DeviceResponse
from app.schemas.railway_crossing import RailwayCrossingResponse
from app.schemas.railway_division import RailwayDivisionResponse
from app.schemas.railway_station import RailwayStationResponse
from app.schemas.railway_zone import RailwayZoneResponse


class HierarchySensorSummary(BaseModel):
    id: int
    sensor_code: str
    sensor_name: str
    status: str
    health_status: str


class HierarchyDeviceNode(BaseModel):
    id: int
    device_code: str
    device_name: str
    device_type: str
    status: str
    health_status: str
    sensors: list[HierarchySensorSummary] = Field(default_factory=list)


class HierarchyCrossingNode(BaseModel):
    id: int
    crossing_code: str
    crossing_name: str
    operational_status: str
    monitoring_status: str
    is_active: bool
    devices: list[HierarchyDeviceNode] = Field(default_factory=list)


class HierarchyStationNode(BaseModel):
    id: int
    station_code: str
    station_name: str
    station_type: str
    is_active: bool
    crossings: list[HierarchyCrossingNode] = Field(default_factory=list)


class HierarchyDivisionNode(BaseModel):
    id: int
    division_code: str
    division_name: str
    is_active: bool
    stations: list[HierarchyStationNode] = Field(default_factory=list)


class HierarchyZoneNode(BaseModel):
    id: int
    zone_code: str
    zone_name: str
    is_active: bool
    divisions: list[HierarchyDivisionNode] = Field(default_factory=list)


class RailwayHierarchyResponse(BaseModel):
    zones: list[HierarchyZoneNode]
    include_devices: bool
    include_sensors: bool
    note: str = (
        "Summary hierarchy for administrative browsing. "
        "Live sensor readings are not included in this phase."
    )


class CrossingOverviewResponse(BaseModel):
    crossing: RailwayCrossingResponse
    station: Optional[RailwayStationResponse] = None
    division: Optional[RailwayDivisionResponse] = None
    zone: Optional[RailwayZoneResponse] = None
    devices: list[DeviceResponse] = Field(default_factory=list)
    sensor_count: int = 0
    staff_assignment_count: int = 0
    operational_status: str
    monitoring_status: str
    is_active: bool
