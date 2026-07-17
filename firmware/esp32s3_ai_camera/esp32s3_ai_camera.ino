/*
 * Smart Railway Crossing Anomaly Prevention System
 * Module: ESP32-S3 AI Camera Controller
 *
 * Phase E0 — Safe starter sketch only.
 * - No camera libraries (exact board model unknown)
 * - No camera pin definitions in use
 * - No image capture
 * - Heartbeat via millis() (non-blocking)
 *
 * PENDING: Exact ESP32-S3 AI Camera Board verification.
 * Do not select a final Arduino board target until the product is confirmed.
 *
 * Firmware Version: 0.1.0
 */

#include <Arduino.h>

#if __has_include("../common/include/firmware_constants.h")
#include "../common/include/firmware_constants.h"
#else
#define SERIAL_BAUD_RATE 115200
#define HEARTBEAT_INTERVAL_MS 5000UL
#define FIRMWARE_VERSION_STRING "0.1.0"
#endif

static unsigned long lastHeartbeatMs = 0;
static unsigned long heartbeatCount = 0;

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  delay(500); /* Brief settle for USB Serial. */

  Serial.println();
  Serial.println(F("========================================"));
  Serial.println(F("Project: Smart Railway Crossing Anomaly Prevention System"));
  Serial.println(F("Module: ESP32-S3 AI Camera Controller"));
  Serial.println(F("Firmware Version: 0.1.0"));
  Serial.println(F("Status: Development workspace initialized"));
  Serial.println(F("Exact Camera Board Model: PENDING VERIFICATION"));
  Serial.println(F("Hardware Configuration: Pending exact component verification"));
  Serial.println(F("========================================"));
  Serial.println(F("Note: Camera libraries are NOT imported in Phase E0."));
  Serial.println(F("Note: Camera pins are NOT assigned until the board is verified."));
  Serial.println(F("Note: Heavy AI may require backend-assisted processing."));
  Serial.println();

  lastHeartbeatMs = millis();
}

void loop() {
  unsigned long now = millis();

  if ((now - lastHeartbeatMs) >= HEARTBEAT_INTERVAL_MS) {
    lastHeartbeatMs = now;
    heartbeatCount++;

    Serial.print(F("[HEARTBEAT] count="));
    Serial.print(heartbeatCount);
    Serial.print(F(" uptime_ms="));
    Serial.println(now);
  }

  /* Future: camera init (after board verification), capture, lightweight AI. */
}
