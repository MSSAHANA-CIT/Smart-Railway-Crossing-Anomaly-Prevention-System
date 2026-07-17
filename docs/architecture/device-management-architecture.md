# Device Management Architecture

## Purpose

Explain how field hardware and planned sensors are registered, assigned to crossings, and tracked administratively before live telemetry exists.

## Device Registration

1. Administrator submits device metadata (`device_code`, type, optional serial/MAC).
2. System stores the device as `REGISTERED` with health `UNKNOWN`.
3. Registration does **not** imply the physical device is online, healthy, or installed.
4. Secrets must never be placed in `configuration` or `metadata_json`.

Supported device types include ESP32 sensor controller, ESP32-S3 AI camera, gate/camera/environment controllers, prototype controller, and other.

## Crossing Assignment

- A device may be unassigned (`crossing_id` null) after registration.
- Assignment validates that the crossing exists.
- A device cannot be assigned to two crossings at once; reassignment requires unassign first.
- Unassignment preserves the device record and history.

## Sensor Registration

- Sensors require a valid `sensor_type_id` (catalog from Phase S2) and parent `device_id`.
- Crossing is derived from the device when omitted, or validated when supplied.
- `gpio_reference` is a provisional descriptive label only — not a verified pin mapping.
- Sensor registration does not mean the sensor is physically installed or calibrated.

## Status Tracking

| Field | Meaning |
|-------|---------|
| `status` | Administrative lifecycle (REGISTERED, ACTIVE, MAINTENANCE, …) |
| `health_status` | Observed/manual health (UNKNOWN until telemetry/admin update) |
| `is_active` | Soft enable/disable flag |

## Health Tracking

- Defaults to `UNKNOWN` at registration
- Manual health updates allowed for prototype/admin testing
- Future heartbeat phase will update `last_seen_at` and health automatically

## Future Heartbeat Support

Planned (not in S4):

- Periodic device check-ins
- Automatic ONLINE/OFFLINE transitions
- Telemetry correlation with sensors

## Future Firmware Support

Planned (not in S4):

- Firmware version reporting from devices
- OTA/firmware artifact management
- Secure device credentials (outside JSON configuration blobs)

## Related Documents

- `docs/architecture/railway-organization-architecture.md`
- `docs/embedded/hardware-to-backend-integration-plan.md`
- `docs/phase-documentation/phase-s4-railway-organization-and-device-management.md`
