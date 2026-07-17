# Exact Board Verification Checklist

Use this checklist **before** assigning GPIO pins, selecting final Arduino board targets, or writing camera initialization code.

**Rule:** Do not guess hardware pins. Do not assume the ESP32-S3 camera board model.

---

## ESP32 DevKit V1

- [ ] Front photo captured
- [ ] Back photo captured
- [ ] Pin labels readable in photos / notes
- [ ] USB connector type recorded (USB-C / Micro-USB / other)
- [ ] Board name printed on module recorded
- [ ] USB-to-serial chip identified (if labeled: CP210x, CH340, etc.)
- [ ] Number of pins recorded
- [ ] Operating voltage noted (typically 3.3 V logic)
- [ ] Product link saved

**Notes / evidence location:**  
_Add links or file paths here after purchase._

---

## ESP32-S3 AI Camera Board

**Do not assume** ESP32-S3-EYE, XIAO ESP32S3 Sense, Waveshare, Freenove, ESP32-S3 CAM, or any other specific model.

- [ ] Exact model / product name recorded
- [ ] Front photo captured
- [ ] Back photo captured
- [ ] Camera sensor name recorded (for example OV2640 / OV5640 / other — only after reading the listing or docs)
- [ ] Flash size recorded (8 MB / 16 MB / other)
- [ ] PSRAM size recorded (none / 2 MB / 8 MB / other)
- [ ] USB connector type recorded
- [ ] Antenna type recorded (PCB / external / both)
- [ ] Pin labels documented
- [ ] Product link saved
- [ ] Manufacturer documentation saved

**Pending verification note:** ESP32-S3 board-specific pin mapping remains **blocked** in `firmware/esp32s3_ai_camera/include/camera_pin_config.h` until this section is complete.

**Notes / evidence location:**  
_Add links or file paths here after purchase._

---

## Sensors and actuators

Complete one block per module (duplicate as needed).

### Module: ________________

- [ ] Front photo
- [ ] Back photo
- [ ] Pin labels
- [ ] Module model
- [ ] Voltage markings (3.3 V / 5 V / both)
- [ ] Wire colors (if pre-wired)
- [ ] Product link

Planned inventory reminder:

- 2 × IR break-beam pairs
- 1 × HC-SR04 ultrasonic
- 1 × HC-SR501 PIR
- 1 × SW-420 vibration
- 1 × Rain sensor
- 1 × LDR light sensor
- 1 × SG90 servo
- 1 × Active buzzer
- LEDs (red / yellow / green)
- Breadboard, jumpers, power source

Supporting items to verify when available:

- USB data cables
- LED resistors (220 Ω or 330 Ω)
- HC-SR04 Echo voltage-divider resistors
- External regulated 5 V servo supply
- Multimeter
- Common-ground wiring plan

---

## Sign-off

| Field | Value |
|-------|-------|
| Verified by | |
| Date | |
| Safe to assign sensor GPIO? | No / Yes |
| Safe to enable camera pins? | No / Yes |
| Arduino board targets selected | |

Until sign-off is **Yes**, keep pin headers as placeholders and keep starter sketches free of output control.
