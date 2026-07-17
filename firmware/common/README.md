# Common Firmware Headers

Shared conceptual headers used by both ESP32 controllers.

## Contents

| File | Purpose |
|------|---------|
| `include/communication_protocol.h` | Planned message types and lightweight protocol structures |
| `include/data_models.h` | Future shared telemetry model |
| `include/firmware_constants.h` | Safe version, baud, timeout, and retry constants |

## Status

These headers are **documentation-oriented foundations** for future phases. They do not implement networking, sensor drivers, or camera capture.

## Usage

Arduino sketches may `#include` these headers once relative include paths are configured, or by copying shared definitions into each sketch as needed during early bring-up.

Do not add secrets or Wi-Fi credentials here.
