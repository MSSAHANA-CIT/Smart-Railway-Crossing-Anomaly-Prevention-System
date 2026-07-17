# ESP32 Sensor Controller

Firmware for the **ESP32 DevKit V1** multi-sensor railway crossing controller.

## Status

**Phase E0 — Development workspace initialized.**

- Starter sketch prints identity and a non-blocking heartbeat.
- **No physical hardware has been tested yet.**
- **Final GPIO pins are not assigned.**
- Sensor drivers and actuators are **not implemented**.

## Planned Responsibilities

Eventually this board will handle:

- IR entry beam and IR exit beam
- Ultrasonic distance (HC-SR04)
- PIR motion (HC-SR501)
- Vibration (SW-420)
- Rain level and ambient light (LDR)
- Red, yellow, and green LEDs
- Active buzzer
- SG90 servo gate control
- Device heartbeat and sensor status
- Communication with the backend and/or camera controller

## Folder Layout

```
esp32_sensor_controller/
├── esp32_sensor_controller.ino
├── include/
│   ├── pin_config.h                 # Placeholders only
│   └── device_config.example.h      # Copy → device_config.h (gitignored)
├── src/                             # Future drivers / helpers
└── tests/                           # Future unit / bench tests
```

## Configuration

1. Copy `include/device_config.example.h` to `include/device_config.h`.
2. Fill local Wi-Fi / backend placeholders on your machine only.
3. Never commit `device_config.h` or real credentials.

## Arduino IDE

1. Open `esp32_sensor_controller.ino` in Arduino IDE 2.
2. Select an ESP32 Dev Module target **after** the board arrives.
3. Set Serial Monitor to **115200**.
4. Compile / upload only when hardware and USB data cable are available.

## Related Docs

- `../../docs/embedded/arduino-ide-setup-macos.md`
- `../../docs/embedded/exact-board-verification-checklist.md`
- `../../docs/embedded/firmware-architecture.md`
- `../../hardware/components-list.md`
