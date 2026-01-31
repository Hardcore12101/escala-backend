from sqlalchemy.orm import Session

from src.app.modules.obligations.models import Obligation
from src.app.modules.obligations.enums import ObligationStatus
from src.app.modules.audit.service import log_event


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
        user_id=str(user.id),
        entity="obligation",
        entity_id=obligation.id,
    )

    return obligation
