"""Audit logging service — failures must not crash the main request."""

from typing import Optional

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.audit_log import AuditLog

logger = get_logger(__name__)

# IAM audit actions
USER_CREATED = "USER_CREATED"
USER_LOGIN_SUCCESS = "USER_LOGIN_SUCCESS"
USER_LOGIN_FAILED = "USER_LOGIN_FAILED"
USER_PROFILE_VIEWED = "USER_PROFILE_VIEWED"
USER_DISABLED = "USER_DISABLED"
USER_ENABLED = "USER_ENABLED"
TOKEN_VALIDATED = "TOKEN_VALIDATED"


def create_audit_log(
    db: Session,
    *,
    actor: str,
    action: str,
    entity_type: str,
    entity_id: Optional[str] = None,
    details: Optional[str] = None,
) -> Optional[AuditLog]:
    """Persist an audit log record. Returns None if logging fails."""
    try:
        record = AuditLog(
            actor=actor,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        logger.exception("Failed to write audit log: action=%s actor=%s", action, actor)
        return None
