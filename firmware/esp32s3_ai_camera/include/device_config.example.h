/**
 * @file device_config.example.h
 * @brief EXAMPLE device configuration for the ESP32-S3 AI camera controller.
 *
 * HOW TO USE:
 * 1. Copy this file to device_config.h in the same folder.
 * 2. Replace placeholders with LOCAL development values only.
 * 3. Never commit device_config.h (it is gitignored).
 * 4. Never print passwords or API keys on Serial.
 *
 * WARNING: Do not put production secrets in firmware source control.
 */

#ifndef DEVICE_CONFIG_H
#define DEVICE_CONFIG_H

/* Wi-Fi — placeholders only */
#ifndef WIFI_SSID
#define WIFI_SSID "YOUR_WIFI_SSID_HERE"
#endif

#ifndef WIFI_PASSWORD
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD_HERE"
#endif

/* Backend — placeholders only */
#ifndef BACKEND_BASE_URL
#define BACKEND_BASE_URL "http://192.168.0.100:8000"
#endif

#ifndef DEVICE_CODE
#define DEVICE_CODE "CAMERA-CONTROLLER-DEV-001"
#endif

#ifndef CROSSING_CODE
#define CROSSING_CODE "CROSSING-DEV-001"
#endif

/* Optional API key placeholder if a future device auth scheme requires it */
#ifndef DEVICE_API_KEY
#define DEVICE_API_KEY "REPLACE_WITH_LOCAL_DEV_KEY_ONLY"
#endif

#endif /* DEVICE_CONFIG_H */
