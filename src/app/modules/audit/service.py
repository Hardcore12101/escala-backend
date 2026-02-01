from sqlalchemy.orm import Session
from uuid import UUID
from src.app.modules.audit.models import AuditLog


def log_event(
    db: Session,
    *,
    action: str,
    user_id: UUID | None,
    entity: str | None = None,
    entity_id: UUID | None = None,
    metadata: dict | None = None,
) -> None:
    log = AuditLog(
        action=action,
        user_id=user_id,
        entity=entity,
        entity_id=entity_id,
        metadata=metadata,
    )

    db.add(log)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
