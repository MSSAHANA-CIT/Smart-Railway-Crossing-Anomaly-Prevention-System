/**
 * @file pin_config.h
 * @brief Placeholder pin declarations for the ESP32 DevKit V1 sensor controller.
 *
 * DO NOT ASSIGN FINAL GPIO NUMBERS IN THIS PHASE.
 *
 * Final values depend on:
 * - Exact ESP32 DevKit version and silkscreen labels
 * - Sensor voltage requirements (3.3 V vs 5 V)
 * - Boot-sensitive pins (strapping pins)
 * - Input-only pins on ESP32
 * - PWM requirements (servo, LEDs)
 * - Camera-board communication method (GPIO, UART, etc.)
 *
 * Update this file only after completing:
 * docs/embedded/exact-board-verification-checklist.md
 */

#ifndef PIN_CONFIG_H
#define PIN_CONFIG_H

#include <stdbool.h>

/* -------------------------------------------------------------------------- */
/* Pending verification — placeholders only                                   */
/* Use a sentinel value so accidental digitalWrite() is obvious in review.    */
/* -------------------------------------------------------------------------- */

#ifndef PIN_PENDING
#define PIN_PENDING (-1)
#endif

/* IR break-beam pairs (entry / exit) — GPIO TBD */
static const int PIN_IR_ENTRY = PIN_PENDING;
static const int PIN_IR_EXIT = PIN_PENDING;

/* HC-SR04 ultrasonic — GPIO TBD (Echo may need voltage divider) */
static const int PIN_ULTRASONIC_TRIG = PIN_PENDING;
static const int PIN_ULTRASONIC_ECHO = PIN_PENDING;

/* HC-SR501 PIR — GPIO TBD */
static const int PIN_PIR = PIN_PENDING;

/* SW-420 vibration — GPIO TBD */
static const int PIN_VIBRATION = PIN_PENDING;

/* Rain sensor — GPIO TBD (analog or digital depending on module) */
static const int PIN_RAIN = PIN_PENDING;

/* LDR light sensor — GPIO TBD (often ADC) */
static const int PIN_LDR = PIN_PENDING;

/* Status LEDs — GPIO TBD (use current-limiting resistors) */
static const int PIN_LED_RED_1 = PIN_PENDING;
static const int PIN_LED_RED_2 = PIN_PENDING;
static const int PIN_LED_YELLOW_1 = PIN_PENDING;
static const int PIN_LED_YELLOW_2 = PIN_PENDING;
static const int PIN_LED_GREEN_1 = PIN_PENDING;
static const int PIN_LED_GREEN_2 = PIN_PENDING;

/* Active buzzer — GPIO TBD */
static const int PIN_BUZZER = PIN_PENDING;

/* SG90 servo signal — GPIO TBD (prefer external 5 V supply + common ground) */
static const int PIN_SERVO = PIN_PENDING;

/**
 * Helper: returns true if a pin placeholder has not been assigned yet.
 * Future drivers should refuse to configure pins that are still pending.
 */
static inline bool pin_is_pending(int pin) {
  return pin < 0;
}

#endif /* PIN_CONFIG_H */
