from sqlalchemy.orm import Session
from src.app.modules.guides.models import Guide
from src.app.services.pdf.renderer import render_guide_pdf


def generate_guide_pdf(db: Session, guide_id: int) -> str:
    guide = db.query(Guide).filter(Guide.id == guide_id).first()

    if not guide:
        raise ValueError("Guia não encontrada")

    return render_guide_pdf(
        guide_id=guide.id,
        company_name=guide.company.name,
        company_cnpj=guide.company.cnpj,
        tax_type=guide.guide_type,
        competence=guide.competence,
        amount=guide.amount,
        due_date=guide.due_date,
    )
