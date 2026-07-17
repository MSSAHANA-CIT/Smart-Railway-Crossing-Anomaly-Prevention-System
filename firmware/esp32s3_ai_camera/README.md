# ESP32-S3 AI Camera Controller

Firmware for the **ESP32-S3 AI Camera Board** (exact model **pending verification**).

## Status

**Phase E0 — Development workspace initialized.**

- Starter sketch prints identity and a non-blocking heartbeat.
- **No physical hardware has been tested yet.**
- **Exact board model is unknown** — do not assume ESP32-S3-EYE, XIAO Sense, Waveshare, Freenove, ESP32-S3 CAM, or any other specific product.
- Camera libraries are **not** imported.
- Camera pins are **not** assigned.

## Pending Board Verification

Before any camera initialization code:

1. Collect exact product name, photos, flash/PSRAM specs, and camera sensor model.
2. Complete `docs/embedded/exact-board-verification-checklist.md`.
3. Only then select the Arduino board target and define pins in `include/camera_pin_config.h`.

## Planned Responsibilities

Eventually this board will handle:

- Camera initialization and image capture
- Visual event verification
- Lightweight object or anomaly detection
- Evidence image capture and event metadata
- Device heartbeat
- Communication with the backend
- Possible coordination with the sensor controller

Heavy AI models may not run on every ESP32-S3 camera board. Future options include TinyML, lightweight classification, motion/frame-difference detection, backend-assisted AI, or a combination.

## Folder Layout

```
esp32s3_ai_camera/
├── esp32s3_ai_camera.ino
├── include/
│   ├── camera_pin_config.h          # Protected until board verified
│   └── device_config.example.h
├── src/
├── models/                          # Future TinyML assets
└── tests/
```

## Configuration

1. Copy `include/device_config.example.h` to `include/device_config.h`.
2. Fill local placeholders only; never commit secrets.

## Arduino IDE

Compile as a basic ESP32 program only when a compatible generic target is appropriate for bring-up. Do **not** lock the exact ESP32-S3 camera target until the board is purchased and verified.

Serial Monitor: **115200** baud.

## Related Docs

- `../../docs/embedded/exact-board-verification-checklist.md`
- `../../docs/embedded/esp32-board-support-setup.md`
- `../../docs/embedded/firmware-architecture.md`
