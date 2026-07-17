# Firmware Security Guidelines

Rules for keeping railway crossing firmware safe during development and future deployment.

---

## Credentials and secrets

1. **Never commit Wi-Fi passwords** to GitHub.
2. **Never hardcode production API keys** in `.ino` or header files that are tracked by Git.
3. **Use example configuration files** such as `device_config.example.h`.
4. Keep real values only in local files that are gitignored:
   - `device_config.h`
   - `secrets.h`
   - `wifi_credentials.h`
   - `firmware_secrets.h`
5. **Do not expose secrets through Serial output.** Print connection state, not passwords.

## Device identity

- Use distinct device codes for sensor and camera controllers.
- Register devices with the backend using identities that can be rotated.
- Prefer short-lived or rotatable credentials when the backend supports them.

## Network and TLS (future production)

- In production deployments, **validate backend TLS certificates**.
- Avoid shipping firmware that silently accepts any certificate.
- Use HTTPS endpoints when the deployment environment supports them.

## Command safety

- **Validate commands before operating actuators** (servo, buzzer, LEDs).
- Reject malformed, unauthorized, or out-of-range commands.
- **Log rejected commands** (locally and/or via backend error/audit paths).
- Prefer acknowledge (`MSG_COMMAND_ACKNOWLEDGEMENT`) with success/failure reasons.

## Configuration protection

- Treat firmware configuration as sensitive.
- Limit who can change device config in the field.
- Document any temporary prototype credentials and remove them before production.

## Local prototype credentials

During early lab testing only:

- Use a private Wi-Fi network when possible.
- Use non-production backend URLs.
- Rotate or delete prototype passwords after the lab phase.

## Git hygiene checklist

Before every commit:

- [ ] No real SSID/password in tracked files
- [ ] No API keys in tracked files
- [ ] Only `*.example.h` config templates are committed
- [ ] No `*.bin` / `*.elf` / `*.map` build artifacts

---

## Related documents

- [Hardware-to-Backend Integration Plan](hardware-to-backend-integration-plan.md)
- [Embedded Development Workflow](embedded-development-workflow.md)
- Project root `.gitignore`
