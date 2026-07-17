/*
 * Smart Railway Crossing Anomaly Prevention System
 * Module: ESP32 Sensor Controller (ESP32 DevKit V1)
 *
 * Phase E0 — Safe starter sketch only.
 * - No sensor libraries
 * - No final GPIO assignments
 * - No physical output control
 * - Heartbeat via millis() (non-blocking)
 *
 * Firmware Version: 0.1.0
 */

#include <Arduino.h>

/* Safe shared constants (relative path for Arduino IDE when opened from this folder). */
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
  delay(500); /* Brief settle for USB Serial on many ESP32 boards. */

  Serial.println();
  Serial.println(F("========================================"));
  Serial.println(F("Project: Smart Railway Crossing Anomaly Prevention System"));
  Serial.println(F("Module: ESP32 Sensor Controller"));
  Serial.println(F("Firmware Version: 0.1.0"));
  Serial.println(F("Status: Development workspace initialized"));
  Serial.println(F("Hardware Configuration: Pending exact component verification"));
  Serial.println(F("========================================"));
  Serial.println(F("Note: Final GPIO pins are NOT assigned in Phase E0."));
  Serial.println(F("Note: No sensors or actuators are controlled yet."));
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

  /* Future: non-blocking sensor polling, health checks, and networking. */
}
