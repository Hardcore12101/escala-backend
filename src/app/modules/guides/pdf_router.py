from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.guides.pdf import generate_guide_pdf

router = APIRouter(prefix="/guides", tags=["Guides"])


@router.get("/{guide_id}/pdf")
def download_pdf(
    guide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pdf_bytes = generate_guide_pdf(db, guide_id)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=guia_{guide_id}.pdf"
        },
    )
