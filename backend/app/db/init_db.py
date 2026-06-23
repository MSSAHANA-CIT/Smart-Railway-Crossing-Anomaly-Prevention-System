"""Database connection utilities."""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine


def test_database_connection() -> tuple[bool, str]:
    """
    Test PostgreSQL connectivity using the configured engine.

    Returns:
        A tuple of (success, message).
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True, "Database connection successful"
    except SQLAlchemyError as exc:
        return False, f"Database connection failed: {exc}"
