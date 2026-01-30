from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.modules.apurations.models import Apuration
from app.modules.guides.models import Guide
from app.models.company import Company
from app.modules.audit.service import log_event
from app.services.pdf.guide_pdf import generate_guide_pdf


def generate_guide(
    db: Session,
    apuration_id: int,
    guide_type: str,
    due_date: date,
):
    # 1️⃣ Buscar apuração (precisa estar FECHADA)
    apuration = (
        db.query(Apuration)
        .filter(
            Apuration.id == apuration_id,
            Apuration.status == "CLOSED",
        )
        .first()
    )

    if not apuration:
        raise HTTPException(
            status_code=400,
            detail="Apuração não encontrada ou não fechada",
        )

    # 2️⃣ Buscar empresa vinculada à apuração
    company = (
        db.query(Company)
        .filter(Company.id == apuration.company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada",
        )

    # 3️⃣ Criar guia (SEM PDF ainda)
    guide = Guide(
        apuration_id=apuration.id,
        guide_type=guide_type,
        amount=apuration.total_tax,
        due_date=due_date,
        status="OPEN",
    )

    db.add(guide)
    db.commit()
    db.refresh(guide)  # agora guide.id EXISTE

    # 4️⃣ Gerar PDF
    pdf_path = generate_guide_pdf(
        guide_id=guide.id,
        company_name=company.name,
        company_cnpj=company.cnpj,
        tax_type=guide.guide_type,
        competence=apuration.competence,
        amount=guide.amount,
        due_date=guide.due_date,
    )

    # 5️⃣ Salvar caminho do PDF
    guide.pdf_path = pdf_path
    db.commit()
    db.refresh(guide)

    # 6️⃣ Auditoria
    log_event(
        db=db,
        action="GENERATE_GUIDE",
        entity="guide",
        entity_id=guide.id,
    )

    return guide


def pay_guide(
    db: Session,
    guide_id: int,
    paid_at: date,
):
    guide = db.query(Guide).filter(Guide.id == guide_id).first()

    if not guide:
        raise ValueError("Guia não encontrada")

    if guide.status == "PAID":
        raise ValueError("Guia já está paga")

    guide.status = "PAID"
    guide.paid_at = paid_at

    db.commit()
    db.refresh(guide)

    log_event(
        db,
        action="PAY_GUIDE",
        entity="guide",
        entity_id=guide.id,
    )

    return guide