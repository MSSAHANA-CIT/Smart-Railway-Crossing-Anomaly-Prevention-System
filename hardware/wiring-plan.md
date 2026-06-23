# Wiring Plan

> **Status:** Planning document only. Verify pin assignments against actual dev board schematics before assembly.

## ESP32 Sensor Controller (Draft)

| Component | ESP32 Pin (draft) | Notes |
|-----------|-------------------|-------|
| Ultrasonic TRIG | GPIO 5 | |
| Ultrasonic ECHO | GPIO 18 | Voltage divider if 5V sensor |
| IR Sensor OUT | GPIO 19 | Digital input |
| Vibration OUT | GPIO 21 | Digital or analog via ADC |
| Buzzer | GPIO 22 | Via transistor if needed |
| Relay IN | GPIO 23 | |
| Status LED Green | GPIO 25 | |
| Status LED Amber | GPIO 26 | |
| Status LED Red | GPIO 27 | |

## ESP32-S3 AI Camera

- Follow manufacturer camera module pinout (typically dedicated camera pins on S3)
- Separate 5V supply recommended for camera stability
- Keep camera cable away from motor/relay noise

## Power

- Common ground between all modules
- Separate fused 5V rails for MCU and relay coil if relay draws high current
- Add TVS diode / surge protection for outdoor installs (production)

## Safety

- Low-voltage logic only on prototype bench
- Railway barrier/signal interfaces require approved isolation relays and official electrical standards
- Do not connect directly to track signaling without licensed railway engineering approval

## Next Steps

1. Confirm dev board pinout
2. Breadboard prototype on desk
3. Document final pins in firmware `config.h`
4. Update this file with photos and final schematic (Phase 3)
