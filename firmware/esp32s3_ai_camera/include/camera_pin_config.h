/**
 * @file camera_pin_config.h
 * @brief Camera pin placeholders — BLOCKED until exact board verification.
 *
 * PENDING VERIFICATION NOTE
 * -------------------------
 * The ESP32-S3 AI Camera Board model is NOT yet known.
 * Do NOT assume: ESP32-S3-EYE, XIAO ESP32S3 Sense, Waveshare, Freenove,
 * ESP32-S3 CAM, or any other specific model.
 *
 * Different boards use different GPIO maps, flash/PSRAM sizes, USB setups,
 * power pins, and upload procedures.
 *
 * Required before enabling camera pins:
 * - Exact product name
 * - Front and back photographs
 * - Product listing
 * - Flash specification
 * - PSRAM specification
 * - Camera sensor model
 *
 * See: docs/embedded/exact-board-verification-checklist.md
 */

#ifndef CAMERA_PIN_CONFIG_H
#define CAMERA_PIN_CONFIG_H

/**
 * Compile-time gate.
 * Keep this as 0 until the exact board is verified and pins are documented.
 * Camera bring-up code must check this flag before configuring hardware.
 */
#ifndef CAMERA_BOARD_VERIFIED
#define CAMERA_BOARD_VERIFIED 0
#endif

#if CAMERA_BOARD_VERIFIED
#error "CAMERA_BOARD_VERIFIED is set, but final pin values are not filled yet. Assign pins from verified board documentation before enabling."
#endif

/* Sentinel: no real GPIO until verification is complete. */
#ifndef CAMERA_PIN_PENDING
#define CAMERA_PIN_PENDING (-1)
#endif

/* Placeholder camera interface pins — DO NOT USE until board verified. */
static const int CAM_PIN_PWDN = CAMERA_PIN_PENDING;
static const int CAM_PIN_RESET = CAMERA_PIN_PENDING;
static const int CAM_PIN_XCLK = CAMERA_PIN_PENDING;
static const int CAM_PIN_SIOD = CAMERA_PIN_PENDING;
static const int CAM_PIN_SIOC = CAMERA_PIN_PENDING;
static const int CAM_PIN_D7 = CAMERA_PIN_PENDING;
static const int CAM_PIN_D6 = CAMERA_PIN_PENDING;
static const int CAM_PIN_D5 = CAMERA_PIN_PENDING;
static const int CAM_PIN_D4 = CAMERA_PIN_PENDING;
static const int CAM_PIN_D3 = CAMERA_PIN_PENDING;
static const int CAM_PIN_D2 = CAMERA_PIN_PENDING;
static const int CAM_PIN_D1 = CAMERA_PIN_PENDING;
static const int CAM_PIN_D0 = CAMERA_PIN_PENDING;
static const int CAM_PIN_VSYNC = CAMERA_PIN_PENDING;
static const int CAM_PIN_HREF = CAMERA_PIN_PENDING;
static const int CAM_PIN_PCLK = CAMERA_PIN_PENDING;

#if !CAMERA_BOARD_VERIFIED
/* Soft guard for future code that might include this header early. */
#ifndef CAMERA_PINS_UNSAFE_TO_USE
#define CAMERA_PINS_UNSAFE_TO_USE 1
#endif
#endif

#endif /* CAMERA_PIN_CONFIG_H */
