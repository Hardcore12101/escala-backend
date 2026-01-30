from sqlalchemy.orm import Session
from src.app.modules.audit.models import AuditLog


def log_event(
    db: Session,
    action: str,
    entity: str | None = None,
    entity_id: int | None = None,
):
    log = AuditLog(
        action=action,
        entity=entity,
        entity_id=entity_id,
    )
    db.add(log)
    db.commit()
