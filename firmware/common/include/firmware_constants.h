/**
 * @file firmware_constants.h
 * @brief Safe shared constants for Smart Railway Crossing firmware.
 *
 * No secrets, passwords, API keys, or Wi-Fi credentials belong in this file.
 */

#ifndef FIRMWARE_CONSTANTS_H
#define FIRMWARE_CONSTANTS_H

/* -------------------------------------------------------------------------- */
/* Identity                                                                   */
/* -------------------------------------------------------------------------- */

/** Human-readable firmware version for Serial banners and future heartbeat. */
#ifndef FIRMWARE_VERSION_STRING
#define FIRMWARE_VERSION_STRING "0.1.0"
#endif

/** Numeric major.minor.patch for future protocol payloads. */
#ifndef FIRMWARE_VERSION_MAJOR
#define FIRMWARE_VERSION_MAJOR 0
#endif

#ifndef FIRMWARE_VERSION_MINOR
#define FIRMWARE_VERSION_MINOR 1
#endif

#ifndef FIRMWARE_VERSION_PATCH
#define FIRMWARE_VERSION_PATCH 0
#endif

/* -------------------------------------------------------------------------- */
/* Serial                                                                     */
/* -------------------------------------------------------------------------- */

/** Default UART baud rate for Arduino Serial Monitor. */
#ifndef SERIAL_BAUD_RATE
#define SERIAL_BAUD_RATE 115200
#endif

/* -------------------------------------------------------------------------- */
/* Timing                                                                     */
/* -------------------------------------------------------------------------- */

/** Heartbeat interval in milliseconds (non-blocking millis()-based loops). */
#ifndef HEARTBEAT_INTERVAL_MS
#define HEARTBEAT_INTERVAL_MS 5000UL
#endif

/** Default network / connection attempt timeout in milliseconds. */
#ifndef DEFAULT_CONNECTION_TIMEOUT_MS
#define DEFAULT_CONNECTION_TIMEOUT_MS 15000UL
#endif

/** Maximum retry attempts for a single recoverable operation. */
#ifndef MAX_RETRY_COUNT
#define MAX_RETRY_COUNT 3
#endif

#endif /* FIRMWARE_CONSTANTS_H */
