/**
 * @file data_models.h
 * @brief Conceptual shared telemetry model for future sensor reporting.
 *
 * IMPORTANT:
 * - This structure is a FUTURE shared model.
 * - It is NOT transmitted to the backend in Phase E0.
 * - Field meanings may evolve after hardware verification.
 * - Do not treat this as a frozen wire format yet.
 */

#ifndef DATA_MODELS_H
#define DATA_MODELS_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Future sensor telemetry snapshot.
 *
 * Controllers may eventually fill this structure and serialize it for
 * HTTP/JSON, binary frames, or another protocol still under evaluation.
 */
typedef struct {
  char device_id[32];       /**< Device identity string (future registry). */
  char crossing_id[32];     /**< Crossing identity string (future registry). */
  uint32_t timestamp;       /**< Epoch seconds or device uptime seconds (TBD). */
  uint32_t sequence_number; /**< Monotonic packet counter. */

  bool ir_entry_triggered;  /**< IR entry beam broken / triggered. */
  bool ir_exit_triggered;   /**< IR exit beam broken / triggered. */
  float distance_cm;        /**< Ultrasonic distance in centimeters. */
  bool motion_detected;     /**< PIR motion detection flag. */
  bool vibration_detected;  /**< Vibration sensor flag. */
  int rain_value;           /**< Rain sensor raw or scaled reading. */
  int light_value;          /**< LDR ambient light raw or scaled reading. */

  int gate_state;           /**< Gate position / state code (TBD enum). */
  bool buzzer_state;        /**< Whether buzzer is currently active. */
  int risk_level;           /**< Local or backend-assigned risk level (TBD). */

  char firmware_version[16]; /**< e.g. "0.1.0" */
} SensorTelemetry;

#ifdef __cplusplus
}
#endif

#endif /* DATA_MODELS_H */
