from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from app.modules.guides.models import Guide

def generate_guide_pdf(db: Session, guide_id: int) -> bytes:
    guide = db.query(Guide).filter(Guide.id == guide_id).first()

    if not guide:
        raise ValueError("Guia não encontrada")

    # TEMPORÁRIO (só para validar fluxo)
    content = f"""
GUIA DE PAGAMENTO

ID: {guide.id}
Tipo: {guide.guide_type}
Valor: {guide.amount}
Vencimento: {guide.due_date}
Status: {guide.status}
"""

    return content.encode("utf-8")
