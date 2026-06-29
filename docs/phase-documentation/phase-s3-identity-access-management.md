# Phase S3 — Identity and Access Management

**Project:** Smart Railway Crossing Anomaly Prevention System  
**Version:** 0.1.3  
**Date:** 2025-06-29

---

## Objective

Build the Identity and Access Management (IAM) foundation for the backend API. This phase establishes secure user authentication, password hashing, JWT access tokens, role-based access structure, protected routes, current user endpoint, user status handling, and audit logging — without frontend login, device management, or sensor APIs.

## Why IAM Is Needed

Railway crossing systems require controlled access for operators, station masters, safety inspectors, and administrators. IAM ensures:

- Only authenticated personnel can access sensitive endpoints
- Passwords are never stored in plain text
- Actions are traceable via audit logs
- Different roles receive appropriate permissions
- Disabled or suspended accounts cannot access the system

## Tables Updated

### `users`

New columns added via migration `add_identity_access_management_fields`:

| Column | Type | Purpose |
|--------|------|---------|
| `password_hash` | VARCHAR(255) | bcrypt password hash |
| `status` | VARCHAR(50) | ACTIVE, INACTIVE, SUSPENDED, PENDING |
| `last_login_at` | TIMESTAMPTZ | Last successful login timestamp |
| `failed_login_attempts` | INTEGER | Failed login counter |

### `audit_logs`

Existing table used for IAM audit events (no schema changes).

## Endpoints Created

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/login` | Authenticate and receive JWT |
| GET | `/api/auth/me` | Current user profile |
| POST | `/api/auth/verify-token` | Validate bearer token |
| POST | `/api/users` | Create user (bootstrap or SUPER_ADMIN) |
| GET | `/api/users` | List users (admin only) |
| GET | `/api/users/{user_id}` | Get user (admin or self) |
| PATCH | `/api/users/{user_id}/disable` | Disable user |
| PATCH | `/api/users/{user_id}/enable` | Enable user |

## Security Features

- **bcrypt password hashing** via passlib CryptContext
- **JWT access tokens** signed with HS256 (`SECRET_KEY`)
- **Token payload:** `sub`, `user_id`, `role`, `exp`
- **Bearer authentication** on protected routes
- **Role-based access control** via `require_roles` dependency
- **Safe API responses** — `password_hash` never exposed
- **Account status checks** — inactive/suspended users cannot login
- **Failed login tracking** — increments `failed_login_attempts`

## Role-Based Access Design

| Endpoint | SUPER_ADMIN | RAILWAY_ADMIN | Self | Public (no users) |
|----------|:-----------:|:-------------:|:----:|:-----------------:|
| POST /api/users | ✓ | | | ✓ |
| GET /api/users | ✓ | ✓ | | |
| GET /api/users/{id} | ✓ | ✓ | ✓ | |
| PATCH disable/enable | ✓ | ✓ | | |
| GET /api/auth/me | ✓ (any auth) | ✓ | ✓ | |

### Roles

`SUPER_ADMIN`, `RAILWAY_ADMIN`, `DIVISION_ADMIN`, `STATION_MASTER`, `CROSSING_OPERATOR`, `MAINTENANCE_ENGINEER`, `SAFETY_INSPECTOR`, `VIEWER`

### Status Values

`ACTIVE`, `INACTIVE`, `SUSPENDED`, `PENDING`

## Audit Logging

Actions logged to `audit_logs`:

| Action | When |
|--------|------|
| `USER_CREATED` | New user created |
| `USER_LOGIN_SUCCESS` | Successful login |
| `USER_LOGIN_FAILED` | Failed login attempt |
| `USER_PROFILE_VIEWED` | User profile accessed |
| `USER_DISABLED` | User account disabled |
| `USER_ENABLED` | User account enabled |
| `TOKEN_VALIDATED` | Token verified via `/api/auth/verify-token` |

Audit logging failures do not crash the main request.

## Testing Procedure

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head

ADMIN_EMAIL=admin@example.com \
ADMIN_FULL_NAME="System Admin" \
ADMIN_PASSWORD="Admin@12345" \
python scripts/create_admin_user.py

uvicorn app.main:app --reload
```

1. **Login** — `POST /api/auth/login` with admin credentials
2. **Current user** — `GET /api/auth/me` with Bearer token
3. **List users** — `GET /api/users` with Bearer token
4. **Verify token** — `POST /api/auth/verify-token` with Bearer token
5. **Failed login** — attempt login with wrong password; check `audit_logs`
6. **Swagger** — use Authorize button with `Bearer <token>`

## Expected Result

- Admin user created with `SUPER_ADMIN` role
- Login returns JWT with `access_token`, `token_type`, `expires_in`, and `user`
- Protected endpoints reject requests without valid token
- User listing restricted to admin roles
- Audit logs record login success and failure events
- Password hash never appears in API responses

## Current Status

**Phase S3 complete.** IAM foundation is operational with JWT authentication, role-based access, and audit logging.

## Next Phase

Phase S4 will add device management APIs and sensor data ingestion endpoints. Frontend login UI will be added in a later frontend phase.
