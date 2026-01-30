from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
from datetime import date


BASE_DIR = Path(__file__).resolve().parents[4]
PDF_DIR = BASE_DIR / "storage" / "guides"
PDF_DIR.mkdir(parents=True, exist_ok=True)


def render_guide_pdf(
    *,
    guide_id: int,
    company_name: str,
    company_cnpj: str,
    tax_type: str,
    competence: str,
    amount: float,
    due_date: date,
) -> str:
    """
    Renderiza o PDF da guia e retorna o caminho do arquivo
    """

    file_name = f"guia_{tax_type}_{competence}_{guide_id}.pdf"
    file_path = PDF_DIR / file_name

    c = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    y = height - 50

    def draw(text, step=20):
        nonlocal y
        c.drawString(50, y, text)
        y -= step

    draw("GUIA DE RECOLHIMENTO", 30)
    draw("-" * 80, 30)

    draw(f"Empresa: {company_name}")
    draw(f"CNPJ: {company_cnpj}")
    draw("")
    draw(f"Tributo: {tax_type}")
    draw(f"Competência: {competence}")
    draw(f"Vencimento: {due_date.strftime('%d/%m/%Y')}")
    draw("")
    draw(f"Valor a pagar: R$ {amount:,.2f}")
    draw("")
    draw("-" * 80)
    draw("Documento gerado automaticamente pelo sistema Escala Digital.")

    c.showPage()
    c.save()

    return str(file_path)
