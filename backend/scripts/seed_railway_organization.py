#!/usr/bin/env python3
"""
Idempotent demonstration seed for Phase S4 railway organization data.

Creates fictional DEMO-* records only. Does not represent real Indian Railways data.
Requires an existing database with migrations applied and sensor types seeded.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Allow running as `python scripts/seed_railway_organization.py` from backend/
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.seed import seed_sensor_types
from app.db.session import SessionLocal
from app.models.device import (
    COMM_SIMULATED,
    DEVICE_TYPE_ESP32_SENSOR_CONTROLLER,
    DEVICE_TYPE_ESP32S3_AI_CAMERA,
    Device,
)
from app.models.railway_crossing import RailwayCrossing
from app.models.railway_division import RailwayDivision
from app.models.railway_station import RailwayStation
from app.models.railway_zone import RailwayZone
from app.models.sensor import Sensor
from app.models.sensor_type import SensorType


def _get_or_create_zone(db: Session) -> tuple[RailwayZone, bool]:
    existing = db.scalar(
        select(RailwayZone).where(RailwayZone.zone_code == "DEMO-ZONE")
    )
    if existing:
        return existing, False
    zone = RailwayZone(
        zone_code="DEMO-ZONE",
        zone_name="Demonstration Railway Zone",
        headquarters="Demo City",
        description="Fictional demonstration zone for college prototype testing.",
        state_coverage="Demo State",
        status="ACTIVE",
        is_active=True,
    )
    db.add(zone)
    db.flush()
    return zone, True


def _get_or_create_division(
    db: Session, zone: RailwayZone
) -> tuple[RailwayDivision, bool]:
    existing = db.scalar(
        select(RailwayDivision).where(RailwayDivision.division_code == "DEMO-DIVISION")
    )
    if existing:
        return existing, False
    division = RailwayDivision(
        division_code="DEMO-DIVISION",
        division_name="Demonstration Division",
        zone_id=zone.id,
        headquarters="Demo Division HQ",
        description="Fictional demonstration division.",
        status="ACTIVE",
        is_active=True,
    )
    db.add(division)
    db.flush()
    return division, True


def _get_or_create_station(
    db: Session, division: RailwayDivision
) -> tuple[RailwayStation, bool]:
    existing = db.scalar(
        select(RailwayStation).where(RailwayStation.station_code == "DEMO-STATION")
    )
    if existing:
        return existing, False
    station = RailwayStation(
        station_code="DEMO-STATION",
        station_name="Demonstration Station",
        division_id=division.id,
        station_type="STANDARD",
        city="Demo City",
        state="Demo State",
        status="ACTIVE",
        is_active=True,
    )
    db.add(station)
    db.flush()
    return station, True


def _get_or_create_crossing(
    db: Session,
    *,
    zone: RailwayZone,
    division: RailwayDivision,
    station: RailwayStation,
) -> tuple[RailwayCrossing, bool]:
    existing = db.scalar(
        select(RailwayCrossing).where(
            RailwayCrossing.crossing_code == "DEMO-CROSSING-001"
        )
    )
    if existing:
        return existing, False
    crossing = RailwayCrossing(
        crossing_code="DEMO-CROSSING-001",
        crossing_name="Demonstration Crossing 001",
        location="Demo Road near Demonstration Station",
        station_id=station.id,
        division_id=division.id,
        zone_id=zone.id,
        crossing_type="MANNED",
        road_name="Demo Road",
        landmark="Near Demo Station East Gate",
        gate_type="PROTOTYPE",
        number_of_tracks=2,
        risk_category="NOT_ASSESSED",
        operational_status="TESTING",
        monitoring_status="NOT_CONFIGURED",
        description="Fictional crossing for prototype device assignment demos.",
        is_active=True,
        status="active",
        country="India",
    )
    db.add(crossing)
    db.flush()
    return crossing, True


def _get_or_create_device(
    db: Session,
    *,
    code: str,
    name: str,
    device_type: str,
    crossing: RailwayCrossing,
) -> tuple[Device, bool]:
    existing = db.scalar(select(Device).where(Device.device_code == code))
    if existing:
        if existing.crossing_id is None:
            existing.crossing_id = crossing.id
        return existing, False
    device = Device(
        device_code=code,
        device_name=name,
        device_type=device_type,
        crossing_id=crossing.id,
        communication_type=COMM_SIMULATED,
        status="REGISTERED",
        health_status="UNKNOWN",
        installation_location="Demonstration mounting point",
        location="Demonstration mounting point",
        is_active=True,
        metadata_json={"demo": True, "note": "Simulated device — not physical hardware"},
    )
    db.add(device)
    db.flush()
    return device, True


def _get_or_create_sensor(
    db: Session,
    *,
    code: str,
    name: str,
    sensor_type: SensorType,
    device: Device,
    crossing: RailwayCrossing,
) -> tuple[Sensor, bool]:
    existing = db.scalar(select(Sensor).where(Sensor.sensor_code == code))
    if existing:
        return existing, False
    sensor = Sensor(
        sensor_code=code,
        sensor_name=name,
        sensor_type_id=sensor_type.id,
        device_id=device.id,
        crossing_id=crossing.id,
        unit=sensor_type.unit,
        status="REGISTERED",
        health_status="UNKNOWN",
        gpio_reference="PROVISIONAL-TBD",
        is_active=True,
        metadata_json={
            "demo": True,
            "gpio_reference_note": "Provisional label — not verified hardware mapping.",
        },
    )
    db.add(sensor)
    db.flush()
    return sensor, True


def seed_railway_organization(db: Optional[Session] = None) -> Dict[str, Any]:
    owns_session = db is None
    session = db or SessionLocal()
    created: List[str] = []
    skipped: List[str] = []

    try:
        seed_sensor_types(session)

        zone, zone_created = _get_or_create_zone(session)
        (created if zone_created else skipped).append("DEMO-ZONE")

        division, div_created = _get_or_create_division(session, zone)
        (created if div_created else skipped).append("DEMO-DIVISION")

        station, stn_created = _get_or_create_station(session, division)
        (created if stn_created else skipped).append("DEMO-STATION")

        crossing, crx_created = _get_or_create_crossing(
            session, zone=zone, division=division, station=station
        )
        (created if crx_created else skipped).append("DEMO-CROSSING-001")

        controller, ctrl_created = _get_or_create_device(
            session,
            code="DEMO-ESP32-CONTROLLER-001",
            name="Demo ESP32 Sensor Controller",
            device_type=DEVICE_TYPE_ESP32_SENSOR_CONTROLLER,
            crossing=crossing,
        )
        (created if ctrl_created else skipped).append("DEMO-ESP32-CONTROLLER-001")

        camera, cam_created = _get_or_create_device(
            session,
            code="DEMO-ESP32S3-CAMERA-001",
            name="Demo ESP32-S3 AI Camera",
            device_type=DEVICE_TYPE_ESP32S3_AI_CAMERA,
            crossing=crossing,
        )
        (created if cam_created else skipped).append("DEMO-ESP32S3-CAMERA-001")

        type_by_code = {
            t.code: t
            for t in session.scalars(select(SensorType)).all()
        }
        planned_sensors = [
            ("DEMO-SENSOR-IR-ENTRY-001", "Demo IR Entry Beam", "IR_ENTRY"),
            ("DEMO-SENSOR-IR-EXIT-001", "Demo IR Exit Beam", "IR_EXIT"),
            ("DEMO-SENSOR-ULTRASONIC-001", "Demo Ultrasonic Distance", "ULTRASONIC"),
            ("DEMO-SENSOR-PIR-001", "Demo PIR Motion", "PIR"),
            ("DEMO-SENSOR-VIBRATION-001", "Demo Vibration", "VIBRATION"),
            ("DEMO-SENSOR-RAIN-001", "Demo Rain Sensor", "RAIN"),
            ("DEMO-SENSOR-LDR-001", "Demo LDR Light", "LDR"),
        ]
        for code, name, type_code in planned_sensors:
            sensor_type = type_by_code.get(type_code)
            if not sensor_type:
                skipped.append(f"{code} (missing sensor type {type_code})")
                continue
            _, sens_created = _get_or_create_sensor(
                session,
                code=code,
                name=name,
                sensor_type=sensor_type,
                device=controller,
                crossing=crossing,
            )
            (created if sens_created else skipped).append(code)

        camera_type = type_by_code.get("CAMERA")
        if camera_type:
            _, cam_sens_created = _get_or_create_sensor(
                session,
                code="DEMO-SENSOR-CAMERA-001",
                name="Demo ESP32-S3 Camera Sensor",
                sensor_type=camera_type,
                device=camera,
                crossing=crossing,
            )
            (created if cam_sens_created else skipped).append("DEMO-SENSOR-CAMERA-001")

        session.commit()
        return {
            "created_count": len(created),
            "skipped_count": len(skipped),
            "created": created,
            "skipped": skipped,
            "note": (
                "All DEMO records are fictional and for prototype demonstration only. "
                "They are not real Indian Railways assets."
            ),
        }
    except Exception:
        session.rollback()
        raise
    finally:
        if owns_session:
            session.close()


def main() -> None:
    print("Seeding demonstration railway organization data...")
    print("(Fictional DEMO records only — not real railway data)")
    summary = seed_railway_organization()
    print(f"Created: {summary['created_count']}")
    for item in summary["created"]:
        print(f"  + {item}")
    print(f"Skipped (already present): {summary['skipped_count']}")
    for item in summary["skipped"]:
        print(f"  = {item}")
    print(summary["note"])


if __name__ == "__main__":
    main()
