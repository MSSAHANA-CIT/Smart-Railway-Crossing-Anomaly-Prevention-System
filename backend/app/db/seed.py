"""Sensor type seed data."""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.sensor_type import SensorType

SENSOR_TYPE_SEED_DATA: List[Dict[str, Any]] = [
    {
        "name": "IR Entry Beam",
        "code": "IR_ENTRY",
        "description": "Infrared beam sensor at crossing entry point",
        "unit": "boolean",
    },
    {
        "name": "IR Exit Beam",
        "code": "IR_EXIT",
        "description": "Infrared beam sensor at crossing exit point",
        "unit": "boolean",
    },
    {
        "name": "Ultrasonic Distance Sensor",
        "code": "ULTRASONIC",
        "description": "Ultrasonic sensor for obstacle distance measurement",
        "unit": "cm",
    },
    {
        "name": "PIR Motion Sensor",
        "code": "PIR",
        "description": "Passive infrared motion detection sensor",
        "unit": "boolean",
    },
    {
        "name": "Vibration Sensor",
        "code": "VIBRATION",
        "description": "Vibration sensor for train approach detection",
        "unit": "g",
    },
    {
        "name": "Rain Sensor",
        "code": "RAIN",
        "description": "Rain detection sensor for weather-aware risk adjustment",
        "unit": "boolean",
    },
    {
        "name": "LDR Light Sensor",
        "code": "LDR",
        "description": "Light-dependent resistor for ambient light level",
        "unit": "lux",
    },
    {
        "name": "ESP32-S3 Camera",
        "code": "CAMERA",
        "description": "ESP32-S3 AI camera for visual anomaly detection",
        "unit": None,
    },
]


def seed_sensor_types(db: Optional[Session] = None) -> Dict[str, Any]:
    """
    Insert sensor types only when their code is not already present.

    Returns:
        Summary with counts of inserted and skipped records.
    """
    owns_session = db is None
    session = db or SessionLocal()
    inserted: List[str] = []
    skipped: List[str] = []

    try:
        for entry in SENSOR_TYPE_SEED_DATA:
            code = str(entry["code"])
            existing = session.query(SensorType).filter(SensorType.code == code).first()
            if existing:
                skipped.append(code)
                continue

            session.add(
                SensorType(
                    name=str(entry["name"]),
                    code=code,
                    description=str(entry["description"]) if entry.get("description") else None,
                    unit=str(entry["unit"]) if entry.get("unit") else None,
                    is_active=True,
                )
            )
            inserted.append(code)

        if inserted:
            session.commit()
        elif owns_session:
            session.rollback()

        return {
            "inserted_count": len(inserted),
            "skipped_count": len(skipped),
            "inserted": inserted,
            "skipped": skipped,
        }
    except Exception:
        session.rollback()
        raise
    finally:
        if owns_session:
            session.close()
