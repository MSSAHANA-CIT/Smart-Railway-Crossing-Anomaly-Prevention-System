"""create railway organization and device management

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-07-17

Phase S4 — railway hierarchy, expanded crossings/devices, sensors, staff assignments.
Preserves existing Phase S2 crossings and devices tables (additive changes only).
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, Sequence[str], None] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- railway_zones ---
    op.create_table(
        "railway_zones",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("zone_code", sa.String(length=50), nullable=False),
        sa.Column("zone_name", sa.String(length=255), nullable=False),
        sa.Column("headquarters", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("state_coverage", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["updated_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_railway_zones_zone_code", "railway_zones", ["zone_code"], unique=True)
    op.create_index("ix_railway_zones_status", "railway_zones", ["status"], unique=False)

    # --- railway_divisions ---
    op.create_table(
        "railway_divisions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("division_code", sa.String(length=50), nullable=False),
        sa.Column("division_name", sa.String(length=255), nullable=False),
        sa.Column("zone_id", sa.Integer(), nullable=False),
        sa.Column("headquarters", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["zone_id"], ["railway_zones.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["updated_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_railway_divisions_division_code",
        "railway_divisions",
        ["division_code"],
        unique=True,
    )
    op.create_index("ix_railway_divisions_zone_id", "railway_divisions", ["zone_id"])
    op.create_index("ix_railway_divisions_status", "railway_divisions", ["status"])

    # --- railway_stations ---
    op.create_table(
        "railway_stations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("station_code", sa.String(length=50), nullable=False),
        sa.Column("station_name", sa.String(length=255), nullable=False),
        sa.Column("division_id", sa.Integer(), nullable=False),
        sa.Column(
            "station_type",
            sa.String(length=50),
            nullable=False,
            server_default="STANDARD",
        ),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("district", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("postal_code", sa.String(length=20), nullable=True),
        sa.Column("latitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("contact_phone", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="ACTIVE"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["division_id"], ["railway_divisions.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["updated_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_railway_stations_station_code",
        "railway_stations",
        ["station_code"],
        unique=True,
    )
    op.create_index("ix_railway_stations_division_id", "railway_stations", ["division_id"])
    op.create_index("ix_railway_stations_state", "railway_stations", ["state"])
    op.create_index("ix_railway_stations_status", "railway_stations", ["status"])

    # --- expand crossings (preserve legacy columns) ---
    op.add_column("crossings", sa.Column("station_id", sa.Integer(), nullable=True))
    op.add_column("crossings", sa.Column("division_id", sa.Integer(), nullable=True))
    op.add_column("crossings", sa.Column("zone_id", sa.Integer(), nullable=True))
    op.add_column(
        "crossings",
        sa.Column(
            "crossing_type",
            sa.String(length=50),
            nullable=False,
            server_default="OTHER",
        ),
    )
    op.add_column("crossings", sa.Column("road_name", sa.String(length=255), nullable=True))
    op.add_column("crossings", sa.Column("landmark", sa.String(length=255), nullable=True))
    op.add_column("crossings", sa.Column("latitude", sa.Numeric(10, 7), nullable=True))
    op.add_column("crossings", sa.Column("longitude", sa.Numeric(10, 7), nullable=True))
    op.add_column(
        "crossings",
        sa.Column(
            "gate_type",
            sa.String(length=50),
            nullable=False,
            server_default="PROTOTYPE",
        ),
    )
    op.add_column("crossings", sa.Column("number_of_tracks", sa.Integer(), nullable=True))
    op.add_column(
        "crossings",
        sa.Column(
            "risk_category",
            sa.String(length=50),
            nullable=False,
            server_default="NOT_ASSESSED",
        ),
    )
    op.add_column(
        "crossings",
        sa.Column(
            "operational_status",
            sa.String(length=50),
            nullable=False,
            server_default="TESTING",
        ),
    )
    op.add_column(
        "crossings",
        sa.Column(
            "monitoring_status",
            sa.String(length=50),
            nullable=False,
            server_default="NOT_CONFIGURED",
        ),
    )
    op.add_column("crossings", sa.Column("description", sa.Text(), nullable=True))
    op.add_column(
        "crossings",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.add_column("crossings", sa.Column("created_by_user_id", sa.Integer(), nullable=True))
    op.add_column("crossings", sa.Column("updated_by_user_id", sa.Integer(), nullable=True))

    op.create_foreign_key(
        "fk_crossings_station_id",
        "crossings",
        "railway_stations",
        ["station_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_crossings_division_id",
        "crossings",
        "railway_divisions",
        ["division_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_crossings_zone_id",
        "crossings",
        "railway_zones",
        ["zone_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_crossings_created_by_user_id",
        "crossings",
        "users",
        ["created_by_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_crossings_updated_by_user_id",
        "crossings",
        "users",
        ["updated_by_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_crossings_station_id", "crossings", ["station_id"])
    op.create_index("ix_crossings_division_id", "crossings", ["division_id"])
    op.create_index("ix_crossings_zone_id", "crossings", ["zone_id"])
    op.create_index("ix_crossings_risk_category", "crossings", ["risk_category"])
    op.create_index("ix_crossings_operational_status", "crossings", ["operational_status"])
    op.create_index("ix_crossings_monitoring_status", "crossings", ["monitoring_status"])

    # --- expand devices ---
    op.add_column("devices", sa.Column("serial_number", sa.String(length=100), nullable=True))
    op.add_column("devices", sa.Column("manufacturer", sa.String(length=100), nullable=True))
    op.add_column("devices", sa.Column("model_name", sa.String(length=100), nullable=True))
    op.add_column("devices", sa.Column("hardware_version", sa.String(length=50), nullable=True))
    op.add_column("devices", sa.Column("firmware_version", sa.String(length=50), nullable=True))
    op.add_column("devices", sa.Column("crossing_id", sa.Integer(), nullable=True))
    op.add_column(
        "devices", sa.Column("installation_location", sa.String(length=255), nullable=True)
    )
    op.add_column("devices", sa.Column("mac_address", sa.String(length=50), nullable=True))
    op.add_column("devices", sa.Column("ip_address", sa.String(length=50), nullable=True))
    op.add_column(
        "devices",
        sa.Column(
            "communication_type",
            sa.String(length=50),
            nullable=False,
            server_default="UNKNOWN",
        ),
    )
    op.add_column(
        "devices",
        sa.Column(
            "health_status",
            sa.String(length=50),
            nullable=False,
            server_default="UNKNOWN",
        ),
    )
    op.add_column("devices", sa.Column("registered_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("devices", sa.Column("activated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        "devices", sa.Column("deactivated_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "devices",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.add_column(
        "devices",
        sa.Column("configuration", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column(
        "devices",
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.add_column("devices", sa.Column("created_by_user_id", sa.Integer(), nullable=True))
    op.add_column("devices", sa.Column("updated_by_user_id", sa.Integer(), nullable=True))

    op.create_foreign_key(
        "fk_devices_crossing_id",
        "devices",
        "crossings",
        ["crossing_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_devices_created_by_user_id",
        "devices",
        "users",
        ["created_by_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_devices_updated_by_user_id",
        "devices",
        "users",
        ["updated_by_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_devices_crossing_id", "devices", ["crossing_id"])
    op.create_index("ix_devices_device_type", "devices", ["device_type"])
    op.create_index("ix_devices_status", "devices", ["status"])
    op.create_index("ix_devices_health_status", "devices", ["health_status"])
    op.create_index("ix_devices_last_seen_at", "devices", ["last_seen_at"])
    op.create_index(
        "uq_devices_serial_number",
        "devices",
        ["serial_number"],
        unique=True,
        postgresql_where=sa.text("serial_number IS NOT NULL"),
    )
    op.create_index(
        "uq_devices_mac_address",
        "devices",
        ["mac_address"],
        unique=True,
        postgresql_where=sa.text("mac_address IS NOT NULL"),
    )

    # Normalize legacy device status values toward Phase S4 vocabulary where obvious
    op.execute(
        """
        UPDATE devices
        SET status = CASE
            WHEN lower(status) IN ('offline', 'unknown') THEN 'REGISTERED'
            WHEN lower(status) = 'online' THEN 'ACTIVE'
            WHEN lower(status) = 'fault' THEN 'MAINTENANCE'
            ELSE status
        END
        """
    )

    # --- sensors ---
    op.create_table(
        "sensors",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sensor_code", sa.String(length=100), nullable=False),
        sa.Column("sensor_name", sa.String(length=255), nullable=False),
        sa.Column("sensor_type_id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("crossing_id", sa.Integer(), nullable=True),
        sa.Column("manufacturer", sa.String(length=100), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("measurement_type", sa.String(length=100), nullable=True),
        sa.Column("minimum_value", sa.Numeric(18, 6), nullable=True),
        sa.Column("maximum_value", sa.Numeric(18, 6), nullable=True),
        sa.Column("warning_threshold", sa.Numeric(18, 6), nullable=True),
        sa.Column("critical_threshold", sa.Numeric(18, 6), nullable=True),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="REGISTERED",
        ),
        sa.Column(
            "health_status",
            sa.String(length=50),
            nullable=False,
            server_default="UNKNOWN",
        ),
        sa.Column("installation_position", sa.String(length=255), nullable=True),
        sa.Column("gpio_reference", sa.String(length=100), nullable=True),
        sa.Column(
            "calibration_required",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column("last_calibrated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "configuration", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("updated_by_user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["sensor_type_id"], ["sensor_types.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["crossing_id"], ["crossings.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["updated_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sensors_sensor_code", "sensors", ["sensor_code"], unique=True)
    op.create_index("ix_sensors_sensor_type_id", "sensors", ["sensor_type_id"])
    op.create_index("ix_sensors_device_id", "sensors", ["device_id"])
    op.create_index("ix_sensors_crossing_id", "sensors", ["crossing_id"])
    op.create_index("ix_sensors_status", "sensors", ["status"])
    op.create_index("ix_sensors_health_status", "sensors", ["health_status"])
    op.create_index("ix_sensors_last_seen_at", "sensors", ["last_seen_at"])

    # --- staff_assignments ---
    op.create_table(
        "staff_assignments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("assignment_type", sa.String(length=50), nullable=False),
        sa.Column("zone_id", sa.Integer(), nullable=True),
        sa.Column("division_id", sa.Integer(), nullable=True),
        sa.Column("station_id", sa.Integer(), nullable=True),
        sa.Column("crossing_id", sa.Integer(), nullable=True),
        sa.Column("device_id", sa.Integer(), nullable=True),
        sa.Column("responsibility", sa.Text(), nullable=True),
        sa.Column("shift_name", sa.String(length=100), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("assigned_by_user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["zone_id"], ["railway_zones.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["division_id"], ["railway_divisions.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["station_id"], ["railway_stations.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(["crossing_id"], ["crossings.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["assigned_by_user_id"], ["users.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_staff_assignments_user_id", "staff_assignments", ["user_id"])
    op.create_index(
        "ix_staff_assignments_assignment_type", "staff_assignments", ["assignment_type"]
    )
    op.create_index("ix_staff_assignments_zone_id", "staff_assignments", ["zone_id"])
    op.create_index(
        "ix_staff_assignments_division_id", "staff_assignments", ["division_id"]
    )
    op.create_index(
        "ix_staff_assignments_station_id", "staff_assignments", ["station_id"]
    )
    op.create_index(
        "ix_staff_assignments_crossing_id", "staff_assignments", ["crossing_id"]
    )
    op.create_index("ix_staff_assignments_device_id", "staff_assignments", ["device_id"])
    op.create_index("ix_staff_assignments_is_active", "staff_assignments", ["is_active"])


def downgrade() -> None:
    op.drop_table("staff_assignments")
    op.drop_table("sensors")

    op.drop_index("uq_devices_mac_address", table_name="devices")
    op.drop_index("uq_devices_serial_number", table_name="devices")
    op.drop_index("ix_devices_last_seen_at", table_name="devices")
    op.drop_index("ix_devices_health_status", table_name="devices")
    op.drop_index("ix_devices_status", table_name="devices")
    op.drop_index("ix_devices_device_type", table_name="devices")
    op.drop_index("ix_devices_crossing_id", table_name="devices")
    op.drop_constraint("fk_devices_updated_by_user_id", "devices", type_="foreignkey")
    op.drop_constraint("fk_devices_created_by_user_id", "devices", type_="foreignkey")
    op.drop_constraint("fk_devices_crossing_id", "devices", type_="foreignkey")
    for col in (
        "updated_by_user_id",
        "created_by_user_id",
        "metadata_json",
        "configuration",
        "is_active",
        "deactivated_at",
        "activated_at",
        "registered_at",
        "health_status",
        "communication_type",
        "ip_address",
        "mac_address",
        "installation_location",
        "crossing_id",
        "firmware_version",
        "hardware_version",
        "model_name",
        "manufacturer",
        "serial_number",
    ):
        op.drop_column("devices", col)

    op.drop_index("ix_crossings_monitoring_status", table_name="crossings")
    op.drop_index("ix_crossings_operational_status", table_name="crossings")
    op.drop_index("ix_crossings_risk_category", table_name="crossings")
    op.drop_index("ix_crossings_zone_id", table_name="crossings")
    op.drop_index("ix_crossings_division_id", table_name="crossings")
    op.drop_index("ix_crossings_station_id", table_name="crossings")
    op.drop_constraint("fk_crossings_updated_by_user_id", "crossings", type_="foreignkey")
    op.drop_constraint("fk_crossings_created_by_user_id", "crossings", type_="foreignkey")
    op.drop_constraint("fk_crossings_zone_id", "crossings", type_="foreignkey")
    op.drop_constraint("fk_crossings_division_id", "crossings", type_="foreignkey")
    op.drop_constraint("fk_crossings_station_id", "crossings", type_="foreignkey")
    for col in (
        "updated_by_user_id",
        "created_by_user_id",
        "is_active",
        "description",
        "monitoring_status",
        "operational_status",
        "risk_category",
        "number_of_tracks",
        "gate_type",
        "longitude",
        "latitude",
        "landmark",
        "road_name",
        "crossing_type",
        "zone_id",
        "division_id",
        "station_id",
    ):
        op.drop_column("crossings", col)

    op.drop_table("railway_stations")
    op.drop_table("railway_divisions")
    op.drop_table("railway_zones")
