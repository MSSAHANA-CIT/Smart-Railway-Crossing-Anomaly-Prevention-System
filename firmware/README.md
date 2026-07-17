# Firmware Workspace

**Project:** Smart Railway Crossing Anomaly Prevention System  
**Full title:** Risk-Adaptive Railway Crossing Protection System Using Multi-Sensor Intrusion Analysis and Automated Preventive Response with False Alarm Rejection Engine

---

## Purpose

This folder holds all embedded firmware for the railway crossing protection system. It is organized for Arduino IDE development, GitHub version control, and future connection to the FastAPI backend.

## Planned Two-Controller Architecture

| Controller | Board | Role |
|------------|-------|------|
| Sensor Controller | ESP32 DevKit V1 | Multi-sensor reading, local actuators (LEDs, buzzer, servo), heartbeat, status reporting |
| AI Camera Controller | ESP32-S3 AI Camera Board | Image capture, visual verification, lightweight detection, evidence metadata |

The two boards will eventually coordinate with each other and/or the backend. The final board-to-board protocol is **not yet decided** (Wi-Fi HTTP, ESP-NOW, or serial are under evaluation).

## Board Responsibilities

### ESP32 DevKit V1 — Sensor Controller

Planned (not yet implemented):

- IR entry beam and IR exit beam
- Ultrasonic distance (HC-SR04)
- PIR motion (HC-SR501)
- Vibration (SW-420)
- Rain level and ambient light (LDR)
- Red, yellow, and green LEDs
- Active buzzer and SG90 servo gate control
- Device heartbeat and sensor status
- Communication with backend and/or camera controller

### ESP32-S3 AI Camera Board — Camera Controller

Planned (not yet implemented):

- Camera initialization and image capture
- Visual event verification
- Lightweight object or anomaly detection
- Evidence image capture and event metadata
- Device heartbeat and backend communication
- Possible coordination with the sensor controller

**Note:** Heavy AI models may not run on all ESP32-S3 camera boards. Future design may use TinyML, lightweight classification, motion/frame-difference detection, backend-assisted AI, or a mix of edge and server processing.

## Current Development Status

| Item | Status |
|------|--------|
| Firmware workspace structure | Created (Phase E0) |
| Starter sketches (heartbeat only) | Created |
| Shared headers (protocol, models, constants) | Created (conceptual) |
| Sensor drivers | Not started |
| Camera initialization | Not started |
| Wi-Fi / backend networking | Template only |
| Physical upload / Serial testing | **Not possible yet** |

## Hardware Verification Status

**No physical hardware has been tested yet.**

Boards and sensors have not been purchased or verified. Final GPIO pins are **not assigned**. ESP32-S3 board-specific pin mapping is **pending exact board verification**.

Before writing final pin maps or camera code, the team must complete:

`docs/embedded/exact-board-verification-checklist.md`

Do **not** assume the ESP32-S3 board is ESP32-S3-EYE, XIAO ESP32S3 Sense, Waveshare, Freenove, ESP32-S3 CAM, or any other specific model until product evidence is collected.

## Folder Structure

```
firmware/
├── README.md                          # This file
├── common/                            # Shared headers and future shared logic
│   ├── include/
│   │   ├── communication_protocol.h
│   │   ├── data_models.h
│   │   └── firmware_constants.h
│   └── src/
├── esp32_sensor_controller/           # ESP32 DevKit V1 sketch
│   ├── esp32_sensor_controller.ino
│   ├── include/
│   │   ├── pin_config.h               # Placeholders only
│   │   └── device_config.example.h    # Copy to device_config.h locally
│   ├── src/
│   └── tests/
├── esp32s3_ai_camera/                 # ESP32-S3 camera sketch
│   ├── esp32s3_ai_camera.ino
│   ├── include/
│   │   ├── camera_pin_config.h        # Protected until board verified
│   │   └── device_config.example.h
│   ├── src/
│   ├── models/                        # Future TinyML / model assets
│   └── tests/
└── examples/
    ├── basic_serial_test/
    └── wifi_connection_template/
```

## Arduino IDE Workflow

1. Write and review firmware in Cursor.
2. Save files in this Git repository.
3. Open the `.ino` sketch in Arduino IDE 2.
4. Select the verified board (after hardware arrives).
5. Select the correct USB port.
6. Compile (Verify), then upload.
7. Open Serial Monitor at **115200** baud.
8. Record results and commit only verified changes.

Cursor organizes code. For this beginner phase, **Arduino IDE is the approved tool** for compile, upload, and Serial Monitor. Setup guide: `docs/embedded/arduino-ide-setup-macos.md`.

## Future Backend Integration

Planned path (not implemented in Phase E0):

Sensors → ESP32 DevKit V1 → (camera board and/or) Wi-Fi → FastAPI → PostgreSQL → WebSocket → React dashboard

See `docs/embedded/hardware-to-backend-integration-plan.md`.

## Security Precautions

- Never commit Wi-Fi passwords, API keys, or secrets.
- Use `device_config.example.h` as a template; keep real `device_config.h` local (gitignored).
- Do not print passwords or API keys on Serial.
- Full guidelines: `docs/embedded/firmware-security-guidelines.md`.

## GitHub Workflow

1. Edit firmware in Cursor.
2. Review with `git status` and `git diff`.
3. Commit when the change is intentional and reviewed.
4. Push to GitHub when ready to share.
5. Update daily progress and error logs after hardware tests.

Do not commit build artifacts (`*.bin`, `*.elf`, `*.map`) or secret config files.
