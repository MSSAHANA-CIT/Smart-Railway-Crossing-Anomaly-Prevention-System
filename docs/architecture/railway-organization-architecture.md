# Railway Organization Architecture

## Purpose

Define how railway administrative units are modeled in the Smart Railway Crossing Anomaly Prevention System so devices, sensors, and staff can be attached to the correct operational context.

## Hierarchy Overview

```
Railway Zone
    ↓
Railway Division
    ↓
Railway Station
    ↓
Railway Crossing
    ↓
Registered Devices → Registered Sensors
    ↓
Assigned Railway Staff
```

## Entities

### Railway Zone

Top-level administrative region used for filtering and high-level oversight. Identified by unique `zone_code`.

### Railway Division

Operates under exactly one zone. Deleting a zone must not cascade-delete divisions (RESTRICT).

### Railway Station

Belongs to one division. Optional geographic fields (city, district, state, coordinates) support filtering; coordinates are not required.

### Railway Crossing

Operational focus of monitoring. Linked to station, division, and zone. Hierarchy consistency is validated on write so a station cannot be paired with an unrelated zone.

### Devices and Sensors

Devices may be registered before crossing assignment. Sensors always belong to a device and inherit or validate the device’s crossing.

### Staff Assignments

Connect a user to one organizational resource type (zone, division, station, crossing, or device) with optional responsibility and shift metadata.

## Design Principles

1. **Soft deactivation** over destructive deletes for major railway records
2. **Clear codes** for human-readable identification
3. **Hierarchy integrity** enforced in the service layer
4. **Prototype honesty** — fictional DEMO data only; no claim of Indian Railways integration
5. **Bounded hierarchy APIs** — devices/sensors omitted by default from hierarchy responses

## Data Ownership

| Actor | Owns / manages |
|-------|----------------|
| SUPER_ADMIN / RAILWAY_ADMIN | Full hierarchy |
| DIVISION_ADMIN | Stations and below within baseline role policy |
| STATION_MASTER | Operational status updates for crossings |
| MAINTENANCE_ENGINEER | Device/sensor maintenance statuses |

Assignment-scoped tenancy (only seeing your assigned resources) is planned for a later phase.

## Related Documents

- `docs/architecture/database-architecture.md`
- `docs/architecture/device-management-architecture.md`
- `docs/phase-documentation/phase-s4-railway-organization-and-device-management.md`
