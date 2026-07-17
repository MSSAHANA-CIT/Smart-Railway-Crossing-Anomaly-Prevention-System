# Embedded Development Workflow

How this project develops firmware safely with Cursor, Arduino IDE, and GitHub.

---

## Approved beginner workflow

1. **Write and review firmware in Cursor**  
   Edit sketches and headers under `firmware/`. Keep comments clear. Do not invent GPIO pins.

2. **Save files in the Git repository**  
   Keep work inside the project folder so version control can track it.

3. **Open the sketch in Arduino IDE**  
   Open the `.ino` file from the matching sketch folder (Arduino expects the folder name to match the `.ino` name).

4. **Select the verified board**  
   Choose the board only after hardware verification. Camera board target stays pending until the exact model is known.

5. **Select the correct USB port**  
   Use a USB data cable. Confirm the port under **Tools → Port**.

6. **Compile first (Verify)**  
   Fix errors before uploading.

7. **Fix compilation errors**  
   Read the error line, correct the source in Cursor or Arduino IDE, save, and verify again.

8. **Upload firmware**  
   Only after a clean compile and with hardware connected.

9. **Open Serial Monitor**  
   Set baud to **115200**.

10. **Capture output**  
    Copy important Serial lines into daily progress or error logs.

11. **Record test result**  
    Note pass/fail, board used, cable used, and any unexpected behavior.

12. **Commit only verified changes**  
    Prefer committing after a meaningful review. For hardware tests, commit after a known-good Serial result when practical.

13. **Push to GitHub**  
    Share progress with `git push` when ready (do not push secrets).

14. **Update daily progress and error logs**  
    Keep `docs/daily-progress/` and `docs/error-logs/` current.

---

## Cursor and physical upload

Cursor cannot physically upload firmware unless a separate toolchain (Arduino CLI, PlatformIO, etc.) is installed and configured.

For this beginner phase:

- **Arduino IDE is the approved upload and Serial Monitor tool.**

---

## What is completed vs planned

| Completed (Phase E0) | Planned (later) |
|----------------------|-----------------|
| Firmware folder layout | Sensor drivers |
| Starter heartbeats | Camera init |
| Docs and checklists | Backend device APIs from firmware |
| Example templates | Final pin maps |

**No physical compilation, upload, or hardware validation has been completed because the boards have not yet been received.**

---

## Related documents

- [Arduino IDE Setup (macOS)](arduino-ide-setup-macos.md)
- [ESP32 Board Support Setup](esp32-board-support-setup.md)
- [Hardware-to-Backend Integration Plan](hardware-to-backend-integration-plan.md)
