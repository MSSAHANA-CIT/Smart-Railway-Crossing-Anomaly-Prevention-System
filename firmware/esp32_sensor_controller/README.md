# ESP32 Sensor Controller

Firmware project for the ESP32-based multi-sensor railway crossing controller.

## Status

**Phase 0 — Placeholder only.** No firmware code yet.

## Planned Responsibilities

- Read ultrasonic, IR, and vibration sensors
- Debounce and filter raw readings
- Transmit sensor packets to backend (HTTP/MQTT — TBD)
- Drive local buzzer and status LEDs
- Report device health and connectivity status

## Hardware Reference

See `../../hardware/wiring-plan.md` and `../../hardware/components-list.md`.

## Development Environment

- Arduino IDE or PlatformIO
- Board: ESP32 Dev Module
- Libraries (planned): WiFi, HTTPClient or PubSubClient

## Next Steps (Phase 3)

1. Create `src/main.cpp` and `config.h`
2. Implement sensor drivers on breadboard
3. Serial debug output for calibration
4. Backend ingest endpoint integration
