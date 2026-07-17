# Arduino IDE Setup on macOS (Beginner Guide)

**Project:** Smart Railway Crossing Anomaly Prevention System  
**Audience:** Complete beginners  
**Status:** This guide explains *how* to install Arduino IDE. It does **not** claim Arduino IDE is already installed on your computer.

---

## 1. What is Arduino IDE?

Arduino IDE is a free program that:

- Opens firmware sketches (`.ino` files)
- Compiles (builds) the code for your board
- Uploads the program to the board over USB
- Shows Serial Monitor output from the board

## 2. Why use both Cursor and Arduino IDE?

| Tool | Job |
|------|-----|
| **Cursor** | Write, organize, review, and version-control firmware in the Git repository |
| **Arduino IDE** | Compile, upload, and watch Serial Monitor on real hardware |

Cursor is excellent for editing large projects. Arduino IDE is the approved beginner tool for upload and Serial Monitor in this phase.

## 3. Cursor writes and organizes code

You edit files under `firmware/` in Cursor, keep comments clear, and commit to GitHub when ready.

## 4. Arduino IDE compiles and uploads code

After hardware arrives, you open the same `.ino` sketch in Arduino IDE, select the board and USB port, then click Verify/Upload.

## 5. How to download Arduino IDE 2 for macOS

1. Open a browser and go to the official Arduino software page: [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software)
2. Download **Arduino IDE 2** for macOS.
3. Prefer the official website only (avoid random third-party mirrors).

## 6. How to move it into Applications

1. Open the downloaded `.dmg` disk image.
2. Drag **Arduino IDE** into the **Applications** folder.
3. Eject the disk image when finished.

## 7. How to open it safely on macOS

1. Open **Applications**.
2. Double-click **Arduino IDE**.
3. If macOS shows a security warning, use **System Settings → Privacy & Security** and allow the app if you downloaded it from Arduino’s official site.
4. Complete any first-run prompts.

## 8. Apple Silicon versus Intel Mac

- **Apple Silicon:** Macs with M1, M2, M3, M4 (or newer) chips.
- **Intel:** Older Macs with an Intel processor.

To check:

1. Click the Apple menu → **About This Mac**.
2. Look for Chip (Apple Silicon) or Processor (Intel).

Download the Arduino IDE build that matches your Mac when the site offers a choice.

## 9. How to open Preferences

1. Open Arduino IDE.
2. macOS menu: **Arduino IDE → Settings…** (Arduino IDE 2) or **Preferences**.
3. Note the **Sketchbook location** and **Additional boards manager URLs** fields (used later for ESP32 support).

## 10. How to install ESP32 board support later

ESP32 boards need an extra **Boards Manager** package. Follow:

`docs/embedded/esp32-board-support-setup.md`

Do this when you are ready to compile for ESP32. You do not need a physical board to install the package, but you do need a board to upload.

## 11. How to select a board

1. Connect a board with a **USB data cable** (when hardware arrives).
2. In Arduino IDE: **Tools → Board → …**
3. Choose the board that matches your verified hardware.
4. Do **not** pick a specific ESP32-S3 camera target until the exact product is verified.

## 12. How to select a USB port

1. Plug in the board.
2. **Tools → Port**
3. Select the port that appears for your ESP32 (often includes `usbserial` or `wchusbserial` in the name on macOS).
4. If no port appears, see sections 15–16 below.

## 13. What is Serial Monitor?

Serial Monitor is a window that shows text printed by `Serial.println(...)` from the firmware. It is the main way beginners confirm that a sketch is running.

## 14. How to set Serial Monitor to 115200 baud

1. Open **Tools → Serial Monitor** (or the Serial Monitor icon).
2. Set the baud rate dropdown to **115200**.
3. This project’s starter sketches use 115200.

## 15. USB data cable versus charge-only cable

| Cable type | Can charge? | Can upload firmware? |
|------------|-------------|----------------------|
| USB **data** cable | Yes | Yes |
| Charge-only cable | Yes | **No** |

If the board powers on but no port appears, try a different cable that supports data.

## 16. Why no board or port may appear yet

Before hardware is connected:

- No USB device exists for the computer to list.
- Empty Port menus are normal.
- This project has **not** completed physical testing yet.

## 17. Why not select the exact ESP32-S3 target yet

Different ESP32-S3 camera boards use different pins, flash sizes, PSRAM, and USB setups.

Until you complete:

`docs/embedded/exact-board-verification-checklist.md`

keep the camera target as **pending**. Guessing the wrong board can waste hours on failed uploads and wrong pin maps.

---

## Related documents

- [ESP32 Board Support Setup](esp32-board-support-setup.md)
- [Embedded Development Workflow](embedded-development-workflow.md)
- [Exact Board Verification Checklist](exact-board-verification-checklist.md)
