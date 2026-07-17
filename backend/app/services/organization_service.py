"""Organization hierarchy and crossing overview service."""

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.railway_crossing import RailwayCrossing
from app.models.railway_division import RailwayDivision
from app.models.railway_station import RailwayStation
from app.models.railway_zone import RailwayZone
from app.models.sensor import Sensor
from app.models.staff_assignment import StaffAssignment
from app.schemas.device import DeviceResponse
from app.schemas.organization import (
    CrossingOverviewResponse,
    HierarchyCrossingNode,
    HierarchyDeviceNode,
    HierarchyDivisionNode,
    HierarchySensorSummary,
    HierarchyStationNode,
    HierarchyZoneNode,
    RailwayHierarchyResponse,
)
from app.schemas.railway_crossing import RailwayCrossingResponse
from app.schemas.railway_division import RailwayDivisionResponse
from app.schemas.railway_station import RailwayStationResponse
from app.schemas.railway_zone import RailwayZoneResponse
from app.services.railway_crossing_service import get_crossing_by_id
from app.utils.validation import require_entity


def build_hierarchy(
    db: Session,
    *,
    zone_id: Optional[int] = None,
    division_id: Optional[int] = None,
    station_id: Optional[int] = None,
    include_devices: bool = False,
    include_sensors: bool = False,
) -> RailwayHierarchyResponse:
    """
    Build a bounded summary hierarchy.

    Defaults omit devices/sensors to avoid unbounded nested payloads.
    """
    zone_stmt = select(RailwayZone).order_by(RailwayZone.zone_code.asc())
    if zone_id is not None:
        zone_stmt = zone_stmt.where(RailwayZone.id == zone_id)
    zones = list(db.scalars(zone_stmt))

    zone_nodes: list[HierarchyZoneNode] = []
    for zone in zones:
        division_stmt = (
            select(RailwayDivision)
            .where(RailwayDivision.zone_id == zone.id)
            .order_by(RailwayDivision.division_code.asc())
        )
        if division_id is not None:
            division_stmt = division_stmt.where(RailwayDivision.id == division_id)
        divisions = list(db.scalars(division_stmt))

        division_nodes: list[HierarchyDivisionNode] = []
        for division in divisions:
            station_stmt = (
                select(RailwayStation)
                .where(RailwayStation.division_id == division.id)
                .order_by(RailwayStation.station_code.asc())
            )
            if station_id is not None:
                station_stmt = station_stmt.where(RailwayStation.id == station_id)
            stations = list(db.scalars(station_stmt))

            station_nodes: list[HierarchyStationNode] = []
            for station in stations:
                crossings = list(
                    db.scalars(
                        select(RailwayCrossing)
                        .where(RailwayCrossing.station_id == station.id)
                        .order_by(RailwayCrossing.crossing_code.asc())
                    )
                )
                crossing_nodes: list[HierarchyCrossingNode] = []
                for crossing in crossings:
                    device_nodes: list[HierarchyDeviceNode] = []
                    if include_devices:
                        devices = list(
                            db.scalars(
                                select(Device)
                                .where(Device.crossing_id == crossing.id)
                                .order_by(Device.device_code.asc())
                            )
                        )
                        for device in devices:
                            sensor_summaries: list[HierarchySensorSummary] = []
                            if include_sensors:
                                sensors = list(
                                    db.scalars(
                                        select(Sensor)
                                        .where(Sensor.device_id == device.id)
                                        .order_by(Sensor.sensor_code.asc())
                                    )
                                )
                                sensor_summaries = [
                                    HierarchySensorSummary(
                                        id=s.id,
                                        sensor_code=s.sensor_code,
                                        sensor_name=s.sensor_name,
                                        status=s.status,
                                        health_status=s.health_status,
                                    )
                                    for s in sensors
                                ]
                            device_nodes.append(
                                HierarchyDeviceNode(
                                    id=device.id,
                                    device_code=device.device_code,
                                    device_name=device.device_name,
                                    device_type=device.device_type,
                                    status=device.status,
                                    health_status=device.health_status,
                                    sensors=sensor_summaries,
                                )
                            )
                    crossing_nodes.append(
                        HierarchyCrossingNode(
                            id=crossing.id,
                            crossing_code=crossing.crossing_code,
                            crossing_name=crossing.crossing_name,
                            operational_status=crossing.operational_status,
                            monitoring_status=crossing.monitoring_status,
                            is_active=crossing.is_active,
                            devices=device_nodes,
                        )
                    )
                station_nodes.append(
                    HierarchyStationNode(
                        id=station.id,
                        station_code=station.station_code,
                        station_name=station.station_name,
                        station_type=station.station_type,
                        is_active=station.is_active,
                        crossings=crossing_nodes,
                    )
                )
            division_nodes.append(
                HierarchyDivisionNode(
                    id=division.id,
                    division_code=division.division_code,
                    division_name=division.division_name,
                    is_active=division.is_active,
                    stations=station_nodes,
                )
            )
        zone_nodes.append(
            HierarchyZoneNode(
                id=zone.id,
                zone_code=zone.zone_code,
                zone_name=zone.zone_name,
                is_active=zone.is_active,
                divisions=division_nodes,
            )
        )

    return RailwayHierarchyResponse(
        zones=zone_nodes,
        include_devices=include_devices,
        include_sensors=include_sensors and include_devices,
    )


def get_crossing_overview(db: Session, crossing_id: int) -> CrossingOverviewResponse:
    crossing = require_entity(
        get_crossing_by_id(db, crossing_id), name="Railway crossing"
    )
    assert isinstance(crossing, RailwayCrossing)

    station = (
        db.get(RailwayStation, crossing.station_id) if crossing.station_id else None
    )
    division = (
        db.get(RailwayDivision, crossing.division_id) if crossing.division_id else None
    )
    zone = db.get(RailwayZone, crossing.zone_id) if crossing.zone_id else None

    devices = list(
        db.scalars(
            select(Device)
            .where(Device.crossing_id == crossing.id)
            .order_by(Device.device_code.asc())
        )
    )
    sensor_count = (
        db.scalar(
            select(func.count()).select_from(Sensor).where(
                Sensor.crossing_id == crossing.id
            )
        )
        or 0
    )
    staff_count = (
        db.scalar(
            select(func.count())
            .select_from(StaffAssignment)
            .where(
                StaffAssignment.crossing_id == crossing.id,
                StaffAssignment.is_active.is_(True),
            )
        )
        or 0
    )

    return CrossingOverviewResponse(
        crossing=RailwayCrossingResponse.model_validate(crossing),
        station=RailwayStationResponse.model_validate(station) if station else None,
        division=(
            RailwayDivisionResponse.model_validate(division) if division else None
        ),
        zone=RailwayZoneResponse.model_validate(zone) if zone else None,
        devices=[DeviceResponse.model_validate(d) for d in devices],
        sensor_count=sensor_count,
        staff_assignment_count=staff_count,
        operational_status=crossing.operational_status,
        monitoring_status=crossing.monitoring_status,
        is_active=crossing.is_active,
    )
