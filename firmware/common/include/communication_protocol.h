/**
 * @file communication_protocol.h
 * @brief Planned message types for controller ↔ controller / backend traffic.
 *
 * Phase E0 documents the protocol concept only.
 * Complete networking, framing, and serialization are NOT implemented yet.
 */

#ifndef COMMUNICATION_PROTOCOL_H
#define COMMUNICATION_PROTOCOL_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Planned message type identifiers.
 *
 * Values are placeholders for a future wire protocol. Do not assume these
 * integers are final or already accepted by the FastAPI backend.
 */
typedef enum {
  MSG_DEVICE_BOOT = 1,           /**< Device powered on / firmware started. */
  MSG_HEARTBEAT = 2,             /**< Periodic liveness signal. */
  MSG_SENSOR_READING = 3,        /**< Sensor telemetry snapshot. */
  MSG_SENSOR_HEALTH = 4,         /**< Sensor health / fault report. */
  MSG_CAMERA_EVENT = 5,          /**< Camera visual event / evidence metadata. */
  MSG_RISK_EVENT = 6,            /**< Elevated risk or confirmed anomaly. */
  MSG_ACTUATOR_COMMAND = 7,      /**< Command to LEDs, buzzer, or gate. */
  MSG_COMMAND_ACKNOWLEDGEMENT = 8, /**< Ack / nack for a received command. */
  MSG_ERROR_REPORT = 9           /**< Firmware or hardware error report. */
} MessageType;

/**
 * Lightweight message header concept for future framing.
 * Payload body format is intentionally undefined in Phase E0.
 */
typedef struct {
  uint8_t protocol_version; /**< Protocol version (start at 1 when implemented). */
  uint8_t message_type;     /**< One of MessageType. */
  uint16_t payload_length;  /**< Bytes following this header. */
  uint32_t sequence_number; /**< Monotonic sequence for ordering / dedupe. */
  uint32_t timestamp;       /**< Sender timestamp (definition TBD). */
} ProtocolHeader;

#ifdef __cplusplus
}
#endif

#endif /* COMMUNICATION_PROTOCOL_H */
