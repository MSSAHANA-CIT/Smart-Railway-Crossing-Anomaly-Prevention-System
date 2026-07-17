# Firmware Architecture

**Project:** Smart Railway Crossing Anomaly Prevention System  
**Phase:** E0 foundation (architecture documented; drivers not implemented)

---

## Two-controller design

The system plans two embedded controllers:

1. **ESP32 DevKit V1 — Sensor Controller**  
   Reads intrusion-related sensors and drives local preventive actuators.

2. **ESP32-S3 AI Camera Board — Camera Controller**  
   Captures images, supports visual verification, and may run lightweight detection.

This separation keeps real-time sensor/actuator work independent from camera and vision workloads.

```text
┌─────────────────────┐         ┌──────────────────────────┐
│ ESP32 DevKit V1     │◄───────►│ ESP32-S3 AI Camera Board │
│ Sensor Controller   │  TBD    │ Camera Controller        │
└─────────┬───────────┘         └────────────┬─────────────┘
          │                                  │
          └──────────────┬───────────────────┘
                         │ Wi-Fi / HTTP (planned)
                         ▼
                   FastAPI Backend
                         │
                         ▼
               PostgreSQL + WebSocket
                         │
                         ▼
                 React Dashboard
```

## Sensor controller responsibility

Planned:

- IR entry / exit beams
- Ultrasonic distance, PIR, vibration, rain, light
- LEDs, buzzer, servo gate
- Heartbeat and sensor health
- Telemetry toward backend and/or camera board

## Camera controller responsibility

Planned:

- Camera init and capture (after exact board verification)
- Visual event verification and evidence metadata
- Lightweight on-device detection **if** the board can support it
- Heartbeat and backend communication

Heavy models may run on the server. Edge options may include TinyML, simple classification, or frame-difference motion cues.

## Future communication options

Board-to-board and board-to-backend options under evaluation:

| Option | Use case |
|--------|----------|
| Wi-Fi + HTTP(S) to FastAPI | Primary backend integration path |
| WebSocket (later) | Low-latency dashboard updates via backend |
| ESP-NOW | Possible low-latency board-to-board link |
| UART / serial | Possible short-range wired coordination |

**Engineering decision still open:** final board-to-board protocol is **not chosen yet**. Record evaluation results before locking a design.

## Backend API integration (planned)

Conceptual interactions:

- Device registration
- Heartbeat
- Sensor data ingestion
- Camera evidence upload
- Command retrieval and acknowledgement
- Firmware version reporting
- Error reporting

Details: [hardware-to-backend-integration-plan.md](hardware-to-backend-integration-plan.md)

## Heartbeat

Both starter sketches already print a local Serial heartbeat. Future networked heartbeats will reuse the conceptual `MSG_HEARTBEAT` type in `firmware/common/include/communication_protocol.h`.

## Sensor telemetry

Shared conceptual fields live in `firmware/common/include/data_models.h`.  
**Not transmitted yet.**

## Commands

Future `MSG_ACTUATOR_COMMAND` messages must be validated before moving a servo, sounding a buzzer, or changing signal LEDs. See security guidelines.

## Error reporting

Future `MSG_ERROR_REPORT` messages should include device identity, error code, and safe context (no secrets).

## Offline fallback concept

If Wi-Fi or backend is unavailable, the sensor controller should still be able to perform **local safety responses** (for example local alarm patterns) according to rules defined in a later phase.

## Local safety response concept

Local response means the crossing can still warn using on-site actuators even when cloud services are down. Exact thresholds and sequences are future work.

---

## Related code

- `firmware/README.md`
- `firmware/common/include/communication_protocol.h`
- `firmware/common/include/data_models.h`
- `firmware/esp32_sensor_controller/`
- `firmware/esp32s3_ai_camera/`
