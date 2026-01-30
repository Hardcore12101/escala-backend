from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from datetime import date

from app.modules.guides.models import Guide


def generate_guide_pdf(db: Session, guide_id: int) -> bytes:
    guide = db.query(Guide).filter(Guide.id == guide_id).first()

    if not guide:
        raise ValueError("Guia não encontrada")

    buffer_path = f"/tmp/guide_{guide.id}.pdf"

    c = canvas.Canvas(buffer_path, pagesize=A4)
    width, height = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "GUIA DE PAGAMENTO - DAS")

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Guia ID: {guide.id}")
    c.drawString(50, height - 95, f"Data de emissão: {date.today()}")

    # Conteúdo
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 140, f"Tipo: {guide.guide_type}")
    c.drawString(50, height - 165, f"Valor: R$ {guide.amount}")
    c.drawString(50, height - 190, f"Vencimento: {guide.due_date}")
    c.drawString(50, height - 215, f"Status: {guide.status}")

    # Rodapé
    c.setFont("Helvetica", 8)
    c.drawString(50, 40, "Escala Contabilidade Digital")

    c.showPage()
    c.save()

    with open(buffer_path, "rb") as f:
        return f.read()
