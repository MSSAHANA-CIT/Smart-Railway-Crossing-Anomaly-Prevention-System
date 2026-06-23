# Hardware Architecture

## System Components

### 1. ESP32 Sensor Controller

- **MCU:** ESP32 (Wi-Fi enabled)
- **Sensors (planned):**
  - Ultrasonic distance (crossing zone clearance)
  - Infrared break-beam or PIR (intrusion detection)
  - Vibration sensor (train approach / track activity)
- **Outputs:** Buzzer, relay for barrier/gate signal (Phase 3+)
- **Power:** 5V regulated supply; consider solar + battery for remote crossings

### 2. ESP32-S3 AI Camera Controller

- **MCU:** ESP32-S3 (AI acceleration)
- **Camera:** OV2640 or compatible module
- **Role:** Visual confirmation of intrusions; false alarm rejection input
- **Processing:** On-device inference (TensorFlow Lite / ESP-DL — Phase 4)

### 3. Backend Server

- Development: local machine
- Production: cloud VM or on-premise server at railway division
- PostgreSQL database co-located or managed service

### 4. Operator Workstation

- Standard PC or tablet with modern browser
- Minimum 1280×720 display; touch-friendly UI supported

## Physical Layout (Conceptual)

```
        [ TRACK ]
    ═══════════════════
         CROSSING
    ┌─────────────────┐
    │  Sensor Zone    │  ← Ultrasonic + IR
    │  Camera Mount   │  ← ESP32-S3 elevated view
    └─────────────────┘
    ═══════════════════
        [ TRACK ]

    [ Control Box ]  ← ESP32 + power + relays
    [ Operator PC ]  ← Dashboard (Wi-Fi/LAN)
```

## Connectivity

| Link | Protocol | Notes |
|------|----------|-------|
| Sensors → ESP32 | GPIO / I2C / UART | Bench wiring in Phase 3 |
| ESP32 → Backend | HTTP or MQTT | Wi-Fi; credentials in firmware config |
| Backend → Dashboard | HTTP / WebSocket | LAN or VPN |
| Camera → ESP32-S3 | Parallel / DVP | Module-specific |

## Phase 0 Status

Hardware folders contain planning documents only. No physical assembly or firmware flashing yet.

See also: `hardware/components-list.md`, `hardware/wiring-plan.md`, `hardware/testing-plan.md`.
