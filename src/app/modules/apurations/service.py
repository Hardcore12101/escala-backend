from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from src.app.modules.tax_calculations.models import TaxCalculation
from src.app.modules.apurations.models import Apuration
from src.app.modules.audit.service import log_event


def close_month(
    db: Session,
    company_id: int,
    competence: str,
):
    totals = db.query(
        func.sum(TaxCalculation.base_amount),
        func.sum(TaxCalculation.tax_amount),
    ).join(
        TaxCalculation.obligation
    ).filter(
        TaxCalculation.obligation.has(company_id=company_id),
        TaxCalculation.obligation.has(competence=competence),
    ).first()

    total_base = totals[0] or 0
    total_tax = totals[1] or 0

    apuration = Apuration(
        company_id=company_id,
        competence=competence,
        total_base=total_base,
        total_tax=total_tax,
    )

    db.add(apuration)
    db.commit()
    db.refresh(apuration)

    log_event(
        db,
        action="CLOSE_MONTH",
        entity="apuration",
        entity_id=apuration.id,
    )

    return apuration

def auto_close_apuration_if_paid(db: Session, apuration_id: int):
    apuration = db.query(Apuration).filter(Apuration.id == apuration_id).first()

    if not apuration:
        raise HTTPException(status_code=404, detail="Apuração não encontrada")

    guides = db.query(Guide).filter(
        Guide.apuration_id == apuration_id
    ).all()

    if not guides:
        return  # não fecha se não houver guias

    all_paid = all(g.status == "PAID" for g in guides)

    if all_paid and apuration.status != "CLOSED":
        apuration.status = "CLOSED"
        db.commit()