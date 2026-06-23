# ESP32-S3 AI Camera Controller

Firmware project for the ESP32-S3 camera module with AI-assisted intrusion detection.

## Status

**Phase 0 — Placeholder only.** No firmware or model code yet.

## Planned Responsibilities

- Capture frames from OV2640 (or compatible) camera
- Run edge AI model for person/vehicle/object detection in crossing zone
- Send detection events and thumbnail metadata to backend
- Support false alarm rejection by providing visual confirmation signal
- Operate reliably in outdoor lighting (tuning in Phase 4)

## Hardware Reference

See `../../hardware/wiring-plan.md` and `../../docs/architecture/hardware-architecture.md`.

## Development Environment

- Arduino IDE or PlatformIO
- Board: ESP32-S3 Dev Module
- ESP-DL / TensorFlow Lite for Microcontrollers (evaluation in Phase 4)

## Next Steps (Phase 4)

1. Camera bring-up and live view over serial
2. Collect training/scenario images (compliance permitting)
3. Integrate lightweight detection model
4. Latency and false positive benchmarking
