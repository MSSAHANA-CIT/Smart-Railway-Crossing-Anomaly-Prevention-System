# Hardware Testing Plan

## Phase 3 — Bench Testing (Planned)

### Sensor Controller

| Test | Procedure | Pass Criteria |
|------|-----------|---------------|
| Power-on | Apply 5V | ESP32 boots, serial log visible |
| Ultrasonic | Object at known distance | Reading within ±5 cm |
| IR beam | Break beam | Digital trigger within 100 ms |
| Vibration | Tap sensor | Trigger detected |
| Wi-Fi | Connect to AP | IP assigned, ping OK |
| API ping | POST test payload to backend | HTTP 200 (Phase 3) |

### AI Camera Controller

| Test | Procedure | Pass Criteria |
|------|-----------|---------------|
| Camera init | Boot firmware | Frame capture OK |
| Inference | Person/object in frame | Detection event logged |
| False positive | Empty track scene | No spurious alerts (tuning) |
| Latency | Measure frame-to-event | Target < 2 s (Phase 4) |

## Phase 5 — Integration Testing

- Simulated intrusion: person enters zone → sensors + camera → backend risk elevation → dashboard alert
- False alarm: animal or debris → rejection engine → no critical alert
- Language switch during active alert → labels remain correct

## Safety Tests

- Power loss recovery
- Wi-Fi disconnect / reconnect
- Sensor disconnected → fault status on dashboard

## Documentation

Log all failures in `docs/error-logs/` with photos and serial output.
