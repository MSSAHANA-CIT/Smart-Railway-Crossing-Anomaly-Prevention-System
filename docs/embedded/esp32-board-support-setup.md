# ESP32 Board Support Setup (Arduino IDE)

Beginner guide to installing and using ESP32 board packages in Arduino IDE 2.

**Pending step:** Exact ESP32-S3 board target will be selected **after product verification**. Do not lock a camera board model yet.

---

## Boards Manager

**Boards Manager** installs support for microcontroller families (ESP32, Arduino Uno, etc.).

Path: **Tools → Board → Boards Manager…** (or the Boards Manager icon in the left sidebar in IDE 2).

## ESP32 platform package

1. Open Boards Manager.
2. Search for **esp32** by Espressif Systems.
3. Install the **esp32** platform package.
4. Wait until installation finishes.

You may also need an Additional Boards Manager URL in Preferences if your IDE version requires it. Follow the official Espressif / Arduino ESP32 documentation for the URL that matches your IDE version.

## Board selection

**Tools → Board → esp32 → …**

Examples of names you may see later:

- ESP32 Dev Module (common for ESP32 DevKit V1 bring-up)
- Various ESP32-S3 options (only after exact camera board verification)

**Exact ESP32-S3 board target will be selected after product verification.**

## Port selection

**Tools → Port →** choose the USB serial port for the connected board.

No port is expected until a board is plugged in with a USB **data** cable.

## Upload button

The **Upload** button compiles (if needed) and sends the firmware to the board.

Upload is only possible when:

- Board support is installed
- Correct board is selected
- Correct port is selected
- Hardware is connected

## Verify / Compile button

The **Verify** (checkmark) button compiles without uploading. Always compile first when learning.

## Serial Monitor

Shows text from `Serial.print` / `Serial.println`.

This project uses **115200** baud.

## Library Manager

**Tools → Manage Libraries…** installs extra code libraries (for example, future sensor helpers).

## Board packages versus libraries

| Item | What it is |
|------|------------|
| **Board / platform package** | Teaches Arduino IDE how to compile and upload for a chip family (ESP32) |
| **Library** | Extra code you `#include` for sensors, displays, protocols, etc. |

You need the ESP32 **platform** before ESP32 sketches can compile. Libraries are optional extras.

## Why exact board selection matters

Wrong board selection can cause:

- Failed uploads
- Wrong flash/PSRAM settings
- Wrong default pins
- Confusing Serial / USB behavior

For the ESP32-S3 AI Camera Board, wait for:

- Exact product name
- Photos (front/back)
- Flash and PSRAM specs
- Camera sensor model
- Manufacturer documentation

Checklist: [exact-board-verification-checklist.md](exact-board-verification-checklist.md)

---

## Related documents

- [Arduino IDE Setup (macOS)](arduino-ide-setup-macos.md)
- [Firmware Architecture](firmware-architecture.md)
- [Firmware Security Guidelines](firmware-security-guidelines.md)
