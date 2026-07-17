# Phase S4 — Railway Organization and Device Management

## Phase Title

Railway Organization and Device Management Foundation

## Objective

Build a secure, scalable backend foundation for the railway organizational hierarchy and device/sensor registration so future live sensor ingestion and dashboard monitoring have a coherent administrative model.

## Why This Phase Exists

Phases S1–S3 established the API, database, and identity layers. Before ingesting sensor data, the system must know:

- Which railway zone, division, station, and crossing a device belongs to
- Which sensors are planned under each device
- Which staff members are responsible for which resources

This phase creates that administrative backbone without claiming live hardware connectivity.

## Railway Hierarchy

```
Railway Zone
  └── Railway Division
        └── Railway Station
              └── Railway Crossing
                    └── Registered Devices
                          └── Registered Sensors
                    └── Assigned Railway Staff
```

## Database Tables

| Table | Purpose |
|-------|---------|
| `railway_zones` | Top-level administrative regions |
| `railway_divisions` | Divisions under a zone |
| `railway_stations` | Stations under a division |
| `crossings` | Crossings (Phase S2 table expanded) |
| `devices` | Hardware/simulated controllers (Phase S2 table expanded) |
| `sensors` | Sensors registered under devices |
| `staff_assignments` | User ↔ resource responsibility links |

Legacy Phase S2 columns on `crossings` and `devices` were preserved. Hierarchy foreign keys are additive.

## Relationships

- Zone 1→N Divisions (RESTRICT on zone delete)
- Division 1→N Stations
- Station 1→N Crossings
- Crossing 1→N Devices (SET NULL on crossing delete for devices)
- Device 1→N Sensors
- User 1→N Staff Assignments (typed to zone/division/station/crossing/device)

## API Endpoints

### Railway Zones — `/api/railway/zones`

| Method | Path | Roles |
|--------|------|-------|
| POST | `/` | SUPER_ADMIN, RAILWAY_ADMIN |
| GET | `/` | Authenticated railway roles |
| GET | `/{id}` | Authenticated railway roles |
| PATCH | `/{id}` | SUPER_ADMIN, RAILWAY_ADMIN |
| PATCH | `/{id}/activate` | SUPER_ADMIN, RAILWAY_ADMIN |
| PATCH | `/{id}/deactivate` | SUPER_ADMIN, RAILWAY_ADMIN |

### Railway Divisions — `/api/railway/divisions`

Same pattern; parent zone validated on create/update.

### Railway Stations — `/api/railway/stations`

Write: SUPER_ADMIN, RAILWAY_ADMIN, DIVISION_ADMIN.

### Railway Crossings — `/api/railway/crossings`

Write: SUPER_ADMIN, RAILWAY_ADMIN, DIVISION_ADMIN.  
Operational/monitoring status: also STATION_MASTER.  
Hierarchy integrity validated (station → division → zone).

### Devices — `/api/devices`

Register, list, update, assign/unassign, status, health-status, activate/deactivate, list sensors.

### Sensors — `/api/sensors`

Register under device + sensor type; status/health updates; soft activate/deactivate.

### Staff Assignments — `/api/staff-assignments`

Create/list/update/activate/deactivate; `GET /api/users/{id}/assignments`.

### Organization — `/api/railway`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/hierarchy` | Bounded hierarchy summary |
| GET | `/crossings/{id}/overview` | Crossing + parents + devices + counts |

## Role-Based Access

Baseline role checks are enforced. **Assignment-scoped multi-tenant authorization is documented as future work** and is not claimed complete in this phase.

| Role | Typical access |
|------|----------------|
| SUPER_ADMIN | Full access |
| RAILWAY_ADMIN | Full org/device management |
| DIVISION_ADMIN | Stations, crossings, devices, sensors, assignments |
| STATION_MASTER | Crossing status updates; read hierarchy |
| CROSSING_OPERATOR | Read assigned resources (baseline: read org) |
| MAINTENANCE_ENGINEER | Device/sensor status and health |
| SAFETY_INSPECTOR | Read-focused |
| VIEWER | Read-only |

## Validation Rules

- Unique codes for zones, divisions, stations, crossings, devices, sensors
- Parent entities must exist
- Crossing hierarchy must be consistent
- Device may be assigned to at most one crossing at a time
- Sensor crossing must match device crossing when both set
- Staff assignment requires the resource matching `assignment_type`
- Exact active duplicate staff assignments rejected (409)
- Soft deactivation preferred over hard delete

## Device Registration Design

- Registration sets status `REGISTERED` and health `UNKNOWN`
- Registration does **not** mark hardware healthy or online
- `last_seen_at` remains null until a future heartbeat phase
- `configuration` / `metadata_json` are JSONB; secrets must not be stored
- Simulated communication type supported for prototype demos

## Sensor Registration Design

- Requires valid `sensor_type_id` and `device_id`
- GPIO references are provisional labels only
- Registration does not confirm physical installation
- Thresholds optional

## Staff Assignment Design

- Typed assignments: ZONE, DIVISION, STATION, CROSSING, DEVICE
- Only the relevant FK is stored for the type
- Supports future shift fields without full shift management
- Audited create/update/activate/deactivate

## Audit Logging

Events include zone/division/station/crossing create/update/activate/deactivate, crossing status changes, device register/assign/unassign/status/health, sensor register/status, staff assignment lifecycle.

## Testing

Automated pytest suite under `backend/tests/api/` — **17 tests passed** covering auth, RBAC, hierarchy, devices, sensors, staff assignments, pagination/search, soft deactivate, and S3 auth continuity.

## Expected Results

- Migration applies cleanly on top of S2/S3
- Swagger shows new tagged endpoint groups
- Demo seed creates fictional DEMO-* records only
- Existing auth and health endpoints continue to work

## Actual Results

- Migration `c3d4e5f6a7b8` applied successfully (`alembic upgrade head`)
- Seed script created 14 DEMO records on first run
- `pytest tests/ -v` → **17 passed**
- Application imports with 70 registered routes
- Phase S1–S3 auth endpoints verified via tests

## Limitations

- No live hardware communication or sensor ingestion
- No WebSocket streaming
- No AI risk scoring or FARE
- No resource-level assignment scoping beyond role checks
- No real Indian Railways data; DEMO records are fictional
- No frontend screens for organization management in this phase

## Future Phases

- Live device heartbeat and telemetry ingestion
- Assignment-scoped authorization
- Sensor readings time-series
- Risk scoring and alert workflows
- Dashboard organization UI

## Completion Status

**Phase S4 — Complete** (backend foundation for railway organization and device management)

Prototype disclaimer: This is a college prototype designed around realistic railway operations. It is **not** integrated with Indian Railways production systems.
