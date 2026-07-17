/*
 * Wi-Fi Connection Template
 *
 * TEMPLATE ONLY — not production firmware.
 *
 * SECURITY:
 * - Uses PLACEHOLDER credentials only.
 * - NEVER commit real Wi-Fi passwords to GitHub.
 * - Prefer a local device_config.h (gitignored) for real values.
 * - Do not print the password on Serial.
 *
 * Project: Smart Railway Crossing Anomaly Prevention System
 * Phase: E0 example
 */

#include <Arduino.h>
#include <WiFi.h>

/*
 * Prefer a local config file when you create one:
 *   #include "device_config.h"
 * Until then, placeholders below keep the sketch compilable as a template.
 *
 * Copy firmware/.../include/device_config.example.h → device_config.h
 * and keep secrets out of Git.
 */
#ifndef WIFI_SSID
#define WIFI_SSID "YOUR_WIFI_SSID_HERE"
#endif

#ifndef WIFI_PASSWORD
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD_HERE"
#endif

static const unsigned long WIFI_TIMEOUT_MS = 15000UL;
static const unsigned long STATUS_INTERVAL_MS = 5000UL;

static unsigned long lastStatusMs = 0;

static bool attemptWifiConnect() {
  Serial.println(F("Wi-Fi: starting connection attempt (password not printed)."));
  Serial.print(F("Wi-Fi: SSID="));
  Serial.println(WIFI_SSID);

  if (strcmp(WIFI_SSID, "YOUR_WIFI_SSID_HERE") == 0) {
    Serial.println(F("Wi-Fi: still using placeholders — update local device_config.h"));
    Serial.println(F("Wi-Fi: refusing to connect with example credentials."));
    return false;
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long startMs = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if ((millis() - startMs) >= WIFI_TIMEOUT_MS) {
      Serial.println(F("Wi-Fi: connection TIMEOUT — check SSID/password/range."));
      WiFi.disconnect(true);
      return false;
    }
    delay(250); /* Short waits only while waiting for association. */
    Serial.print('.');
  }

  Serial.println();
  Serial.println(F("Wi-Fi: CONNECTED"));
  Serial.print(F("Wi-Fi: IP="));
  Serial.println(WiFi.localIP());
  return true;
}

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.println();
  Serial.println(F("========================================"));
  Serial.println(F("Wi-Fi Connection Template"));
  Serial.println(F("DO NOT COMMIT REAL CREDENTIALS"));
  Serial.println(F("========================================"));

  attemptWifiConnect();
  lastStatusMs = millis();
}

void loop() {
  unsigned long now = millis();

  if ((now - lastStatusMs) >= STATUS_INTERVAL_MS) {
    lastStatusMs = now;

    wl_status_t status = WiFi.status();
    Serial.print(F("Wi-Fi status="));
    Serial.print(static_cast<int>(status));
    if (status == WL_CONNECTED) {
      Serial.print(F(" IP="));
      Serial.print(WiFi.localIP());
    }
    Serial.println();
  }
}
