#!/usr/bin/env python3
"""Seed the database with reference sensor types."""

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.db.init_db import test_database_connection  # noqa: E402
from app.db.seed import seed_sensor_types  # noqa: E402


def main() -> int:
    connected, message = test_database_connection()
    if not connected:
        print(f"Seed aborted: {message}")
        return 1

    result = seed_sensor_types()
    print("Sensor type seed complete.")
    print(f"  Inserted: {result['inserted_count']} ({', '.join(result['inserted']) or 'none'})")
    print(f"  Skipped:  {result['skipped_count']} ({', '.join(result['skipped']) or 'none'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
