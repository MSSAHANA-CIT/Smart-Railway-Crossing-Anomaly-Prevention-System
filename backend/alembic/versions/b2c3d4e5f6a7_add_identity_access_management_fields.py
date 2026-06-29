"""add_identity_access_management_fields

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2025-06-29

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="ACTIVE",
        ),
    )
    op.add_column(
        "users",
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column(
            "failed_login_attempts",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # Existing rows (if any) need a placeholder hash before NOT NULL constraint
    op.execute(
        "UPDATE users SET password_hash = '' WHERE password_hash IS NULL"
    )
    op.alter_column("users", "password_hash", nullable=False)

    op.alter_column("users", "status", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "failed_login_attempts")
    op.drop_column("users", "last_login_at")
    op.drop_column("users", "status")
    op.drop_column("users", "password_hash")
