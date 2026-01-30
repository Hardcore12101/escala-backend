from datetime import date
from sqlalchemy.orm import Session

from app.modules.obligations.models import Obligation
from app.modules.obligations.enums import ObligationStatus
from app.modules.audit.service import log_event


def update_overdue_obligations(db: Session):
    today = date.today()

    obligations = db.query(Obligation).filter(
        Obligation.status == ObligationStatus.PENDING,
        Obligation.due_date < today,
    ).all()

    for obligation in obligations:
        obligation.status = ObligationStatus.OVERDUE

        log_event(
            db,
            action="OBLIGATION_OVERDUE",
            entity="obligation",
            entity_id=obligation.id,
        )

    db.commit()
