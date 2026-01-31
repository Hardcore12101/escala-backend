from sqlalchemy.orm import Session
from src.app.modules.audit.models import AuditLog


def log_event(
    db: Session,
    *,
    action: str,
    user_id: str,
    entity: str | None = None,
    entity_id: int | None = None,
    metadata: dict | None = None,
):
    log = AuditLog(
        action=action,
        user_id=user_id,
        entity=entity,
        entity_id=entity_id,
        metadata=metadata,
    )
    db.add(log)
    db.commit()
