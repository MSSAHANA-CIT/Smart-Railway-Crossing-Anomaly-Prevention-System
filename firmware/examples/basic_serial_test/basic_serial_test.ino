/*
 * Basic Serial Test
 *
 * Purpose: Minimal first sketch to upload after ESP32 boards arrive.
 * Confirms USB data cable, board power, port selection, and Serial Monitor.
 *
 * - Serial at 115200 baud
 * - Startup message
 * - Increasing counter using millis() (non-blocking interval)
 *
 * Project: Smart Railway Crossing Anomaly Prevention System
 * Phase: E0 example
 */

#include <Arduino.h>

static const unsigned long INTERVAL_MS = 1000UL;
static unsigned long lastPrintMs = 0;
static unsigned long counter = 0;

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println();
  Serial.println(F("Basic Serial Test — startup OK"));
  Serial.println(F("Project: Smart Railway Crossing Anomaly Prevention System"));
  Serial.println(F("Set Serial Monitor baud to 115200."));
  Serial.println();

  lastPrintMs = millis();
}

void loop() {
  unsigned long now = millis();

  if ((now - lastPrintMs) >= INTERVAL_MS) {
    lastPrintMs = now;
    counter++;

    Serial.print(F("count="));
    Serial.print(counter);
    Serial.print(F(" uptime_ms="));
    Serial.println(now);
  }
}
