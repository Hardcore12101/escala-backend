from datetime import date
from sqlalchemy.orm import Session

from src.app.modules.tax_rules.models import TaxRule
from src.app.modules.audit.service import log_event


def create_tax_rule(
    db: Session,
    tax_type: str,
    percentage: float,
    valid_from: date,
):
    # encerra regra vigente anterior
    current = db.query(TaxRule).filter(
        TaxRule.tax_type == tax_type,
        TaxRule.valid_to.is_(None),
    ).first()

    if current:
        current.valid_to = valid_from

    rule = TaxRule(
        tax_type=tax_type,
        percentage=percentage,
        valid_from=valid_from,
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)

    log_event(
        db,
        action="CREATE_TAX_RULE",
        user_id=str(user.id),
        entity="tax_rule",
        entity_id=rule.id,
    )

    return rule
