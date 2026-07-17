# Phase E0 — Embedded Firmware Foundation

## Phase title

Phase E0: Embedded Firmware Workspace and Arduino Development Foundation

## Phase objective

Prepare a professional embedded firmware workspace for:

1. ESP32 DevKit V1 sensor controller
2. ESP32-S3 AI Camera Board
3. Arduino IDE development
4. Future hardware testing
5. Future FastAPI backend connection
6. GitHub version control
7. Phase documentation

## Why this phase was required

Software phases (0, S1–S3) established backend, database, and identity foundations. Embedded work needs a safe, modular firmware tree **before** hardware arrives so that:

- Pin maps are not guessed
- Secrets are not committed
- Beginners have clear Arduino IDE guidance
- Camera board selection stays blocked until verification

## Current project context

| Area | Status |
|------|--------|
| Phase 0 Project Foundation | Complete |
| Phase S1 Backend Foundation | Complete |
| Phase S2 Database Foundation | Complete |
| Phase S3 Identity and Access Management | Complete |
| Phase S4 | Planned / separate |
| Phase E0 Embedded Firmware Foundation | **This phase** |

Backend, frontend, database, and authentication were **not modified** for functional behavior in this phase.

## Folders created

- `firmware/common/` (+ `include/`, `src/`)
- `firmware/esp32_sensor_controller/` (+ `include/`, `src/`, `tests/`)
- `firmware/esp32s3_ai_camera/` (+ `include/`, `src/`, `models/`, `tests/`)
- `firmware/examples/` (+ `basic_serial_test/`, `wifi_connection_template/`)
- `docs/embedded/`

## Files created

### Firmware

- `firmware/README.md`
- `firmware/common/README.md`
- `firmware/common/src/README.md`
- `firmware/common/include/communication_protocol.h`
- `firmware/common/include/data_models.h`
- `firmware/common/include/firmware_constants.h`
- `firmware/esp32_sensor_controller/esp32_sensor_controller.ino`
- `firmware/esp32_sensor_controller/include/pin_config.h`
- `firmware/esp32_sensor_controller/include/device_config.example.h`
- `firmware/esp32_sensor_controller/src/README.md`
- `firmware/esp32_sensor_controller/tests/README.md`
- `firmware/esp32s3_ai_camera/esp32s3_ai_camera.ino`
- `firmware/esp32s3_ai_camera/include/camera_pin_config.h`
- `firmware/esp32s3_ai_camera/include/device_config.example.h`
- `firmware/esp32s3_ai_camera/src/README.md`
- `firmware/esp32s3_ai_camera/models/README.md`
- `firmware/esp32s3_ai_camera/tests/README.md`
- `firmware/examples/README.md`
- `firmware/examples/basic_serial_test/basic_serial_test.ino`
- `firmware/examples/wifi_connection_template/wifi_connection_template.ino`

### Documentation

- `docs/embedded/arduino-ide-setup-macos.md`
- `docs/embedded/esp32-board-support-setup.md`
- `docs/embedded/embedded-development-workflow.md`
- `docs/embedded/exact-board-verification-checklist.md`
- `docs/embedded/firmware-architecture.md`
- `docs/embedded/firmware-security-guidelines.md`
- `docs/embedded/hardware-to-backend-integration-plan.md`
- `docs/phase-documentation/phase-e0-embedded-firmware-foundation.md` (this file)
- `docs/daily-progress/day-embedded-setup-progress.md`

## Starter sketches created

| Sketch | Behavior |
|--------|----------|
| `esp32_sensor_controller.ino` | Serial banner + millis() heartbeat |
| `esp32s3_ai_camera.ino` | Serial banner + pending board notice + heartbeat |
| `basic_serial_test.ino` | Counter for first upload |
| `wifi_connection_template.ino` | Placeholder Wi-Fi template with timeout |

## Documentation created

Arduino IDE setup, ESP32 board support, workflow, exact-board checklist, architecture, security guidelines, hardware-to-backend plan, phase E0 report, daily progress.

## Security decisions

- Example config files only; real `device_config.h` gitignored
- No real Wi-Fi credentials in the repository
- Serial output must not print passwords
- Camera pins gated until board verification
- Sensor pins left as `PIN_PENDING` (-1)

## Exact-board verification requirement

Final pin configuration is allowed only after the user provides product evidence for both boards and modules. Checklist:

`docs/embedded/exact-board-verification-checklist.md`

## Testing status

**No physical compilation, upload, or hardware validation has been completed because the boards have not yet been received.**

Compilation status: **Pending Arduino IDE installation and board availability.**

Static validation only (folder/file presence, no secrets, placeholder pins, sketch structure).

## Limitations

- No sensor drivers
- No camera initialization
- No backend networking from devices
- No final GPIO map
- No claim of upload success

## Pending hardware steps

1. Purchase / receive planned hardware inventory
2. Complete exact-board verification checklist with photos and specs
3. Install Arduino IDE 2 on macOS
4. Install ESP32 board support package
5. Upload `basic_serial_test` first
6. Then bring up controller starter sketches

## Completion status

**Phase E0 workspace and documentation: Complete.**  
**Hardware bring-up: Not started.**

## Next embedded phase (recommended)

Phase E1 (suggested name): Hardware receive, exact-board verification, Arduino IDE install, first Serial upload, provisional pin map draft for ESP32 DevKit V1 only (still no assumed camera board).
