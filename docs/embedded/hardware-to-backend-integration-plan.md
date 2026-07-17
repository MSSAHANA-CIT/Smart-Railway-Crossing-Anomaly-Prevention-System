# Hardware-to-Backend Integration Plan

Future data and control flow between field hardware and the software stack.

**Phase E0 does not implement these APIs in firmware.** Backend routes already exist for health/auth/users; device ingest endpoints may be added in later software phases.

---

## End-to-end flow (planned)

```text
Sensors / actuators
        │
        ▼
ESP32 DevKit V1 (Sensor Controller)
        │
        ├──► ESP32-S3 AI Camera Board (visual verification / evidence)
        │              │
        └──────────────┼──► Wi-Fi
                       ▼
                 FastAPI API
                       │
                       ▼
                  PostgreSQL
                       │
                       ▼
                   WebSocket
                       │
                       ▼
                 React dashboard
```

The sensor controller may also send telemetry **directly** to the backend. Final routing (direct vs camera-relay vs both) remains an engineering decision.

## Planned backend interactions

| Interaction | Purpose |
|-------------|---------|
| Device registration | Register sensor/camera identities and crossing assignment |
| Device heartbeat | Prove the device is alive; report uptime / firmware version |
| Sensor data ingestion | Store multi-sensor readings for risk analysis |
| Camera evidence upload | Store images/metadata for false-alarm review |
| Command retrieval | Pull actuator commands (gate, buzzer, LEDs) |
| Command acknowledgement | Confirm success/failure of actuator actions |
| Firmware version reporting | Track deployed firmware per device |
| Error reporting | Capture faults for maintenance and debugging |

## Mapping to existing software layers

| Layer | Current status (software) | Firmware Phase E0 |
|-------|---------------------------|-------------------|
| FastAPI | Health, IAM foundation present | Not calling APIs yet |
| PostgreSQL | Core tables / migrations present | No device writes from firmware yet |
| WebSocket | Planned / future | Not used |
| React dashboard | Auth + shell present | No live sensor stream yet |

## Message concepts

Shared message type names are documented in:

`firmware/common/include/communication_protocol.h`

Examples: `DEVICE_BOOT`, `HEARTBEAT`, `SENSOR_READING`, `CAMERA_EVENT`, `ACTUATOR_COMMAND`, `ERROR_REPORT`.

## Security notes for integration

- Device credentials must not be committed.
- Production should use certificate validation.
- Commands that move hardware must be authorized and validated.

See [firmware-security-guidelines.md](firmware-security-guidelines.md).

## Implementation order (suggested later phases)

1. Exact board verification and pin assignment
2. Sensor bring-up with Serial-only output
3. Wi-Fi template filled with local lab credentials
4. Heartbeat HTTP call to backend (when endpoint exists)
5. Sensor ingestion
6. Camera evidence path
7. Command channel with acknowledgement
8. Offline local safety fallback

---

## Related documents

- [Firmware Architecture](firmware-architecture.md)
- `../../architecture/system-architecture.md`
- `../../architecture/hardware-architecture.md`
