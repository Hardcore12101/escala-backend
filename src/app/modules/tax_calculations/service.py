from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session

from src.app.modules.tax_rules.models import TaxRule
from src.app.modules.tax_calculations.models import TaxCalculation
from src.app.modules.audit.service import log_event


def calculate_tax(
    db: Session,
    obligation_id: int,
    tax_type: str,
    base_amount: Decimal,
):
    # buscar regra vigente
    rule = db.query(TaxRule).filter(
        TaxRule.tax_type == tax_type,
        TaxRule.valid_from <= date.today(),
        (TaxRule.valid_to.is_(None)) | (TaxRule.valid_to > date.today()),
    ).first()

    if not rule:
        raise ValueError("Nenhuma regra fiscal vigente encontrada")

    tax_amount = (base_amount * rule.percentage) / Decimal(100)

    calculation = TaxCalculation(
        obligation_id=obligation_id,
        tax_rule_id=rule.id,
        base_amount=base_amount,
        percentage=rule.percentage,
        tax_amount=tax_amount,
        calculated_at=date.today(),
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)

    log_event(
        db,
        action="CALCULATE_TAX",
        user_id=str(user.id),
        entity="tax_calculation",
        entity_id=calculation.id,
    )

    return calculation
