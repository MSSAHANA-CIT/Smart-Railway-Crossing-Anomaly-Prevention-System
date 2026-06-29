#!/usr/bin/env python3
"""
Create the first SUPER_ADMIN user for the Smart Railway Crossing system.

Usage (environment variables):
    ADMIN_EMAIL=admin@example.com \\
    ADMIN_FULL_NAME="System Admin" \\
    ADMIN_PASSWORD="YourSecurePassword" \\
    python scripts/create_admin_user.py

If environment variables are not set, the script prints instructions and exits.
Do not hardcode passwords in this script.
"""

import os
import sys

# Allow running from backend/ directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from getpass import getpass

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.user import ROLE_SUPER_ADMIN, STATUS_ACTIVE, User
from app.services.user_service import count_users, get_user_by_email


from typing import Optional, Tuple


def _read_credentials() -> Optional[Tuple[str, str, str]]:
    """Read admin credentials from environment or interactive prompt."""
    email = os.environ.get("ADMIN_EMAIL", "").strip()
    full_name = os.environ.get("ADMIN_FULL_NAME", "").strip()
    password = os.environ.get("ADMIN_PASSWORD", "").strip()

    if email and full_name and password:
        return email, full_name, password

    if not email or not full_name or not password:
        print("=" * 60)
        print("CREATE FIRST SUPER_ADMIN USER")
        print("=" * 60)
        print()
        print("Set the following environment variables:")
        print()
        print('  ADMIN_EMAIL=admin@example.com')
        print('  ADMIN_FULL_NAME="System Admin"')
        print('  ADMIN_PASSWORD="YourSecurePassword"')
        print()
        print("Then run:")
        print("  python scripts/create_admin_user.py")
        print()
        print("Or provide values interactively below.")
        print()

    if not email:
        email = input("Admin email: ").strip()
    if not full_name:
        full_name = input("Full name: ").strip()
    if not password:
        password = getpass("Admin password (min 8 chars): ").strip()
        confirm = getpass("Confirm password: ").strip()
        if password != confirm:
            print("Error: passwords do not match.")
            return None

    if not email or not full_name or not password:
        print("Error: email, full name, and password are required.")
        return None

    if len(password) < 8:
        print("Error: password must be at least 8 characters.")
        return None

    return email, full_name, password


def main() -> int:
    credentials = _read_credentials()
    if not credentials:
        return 1

    email, full_name, password = credentials
    db = SessionLocal()

    try:
        existing = get_user_by_email(db, email)
        if existing:
            print(f"User already exists: {email} (id={existing.id}, role={existing.role})")
            return 0

        total = count_users(db)
        if total > 0:
            print(
                "Users already exist in the database. "
                "Use the API or a SUPER_ADMIN account to create additional users."
            )
            return 1

        user = User(
            email=email,
            full_name=full_name,
            password_hash=get_password_hash(password),
            role=ROLE_SUPER_ADMIN,
            status=STATUS_ACTIVE,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"SUPER_ADMIN created successfully: {user.email} (id={user.id})")
        return 0
    except Exception as exc:
        db.rollback()
        print(f"Error creating admin user: {exc}")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
