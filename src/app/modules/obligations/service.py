from sqlalchemy.orm import Session

from app.modules.obligations.models import Obligation
from app.modules.obligations.enums import ObligationStatus
from app.modules.audit.service import log_event


def create_obligation(
    db: Session,
    company_id: int,
    type,
    competence: str,
    due_date,
):
    obligation = Obligation(
        company_id=company_id,
        type=type,
        competence=competence,
        due_date=due_date,
        status=ObligationStatus.PENDING,
    )

    db.add(obligation)
    db.commit()
    db.refresh(obligation)

    log_event(
        db,
        action="CREATE_OBLIGATION",
        entity="obligation",
        entity_id=obligation.id,
    )

    return obligation
