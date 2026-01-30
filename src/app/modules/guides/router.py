from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from src.app.modules.guides.pdf.generator import generate_guide_pdf

from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.guides.schemas import GuideCreate, GuideResponse
from src.app.modules.guides.service import generate_guide
from src.app.modules.guides.models import Guide
from src.app.modules.guides.schemas import GuideOut, GuidePayRequest
from src.app.modules.guides.service import pay_guide



router = APIRouter(prefix="/guides", tags=["Guides"])


@router.post(
    "",
    response_model=GuideResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_guide(
    data: GuideCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return generate_guide(
        db=db,
        apuration_id=data.apuration_id,
        guide_type=data.guide_type,
        due_date=data.due_date,
    )

@router.get("/{guide_id}/download")
def download_guide(
    guide_id: int,
    db: Session = Depends(get_db)
):
    guide = db.query(Guide).filter(Guide.id == guide_id).first()

    if not guide:
        raise HTTPException(
            status_code=404,
            detail="Guia não encontrada"
        )

    pdf_buffer = generate_guide_pdf(guide)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=guia_{guide_id}.pdf"
        }
    )

@router.get("/", response_model=list[GuideOut])
def list_guides(db: Session = Depends(get_db)):
    return db.query(Guide).all()


@router.patch("/{guide_id}/pay")
def mark_as_paid(
    guide_id: int,
    db: Session = Depends(get_db)
):
    guide = db.query(Guide).filter(Guide.id == guide_id).first()

    if not guide:
        raise HTTPException(status_code=404, detail="Guia não encontrada")

    guide.status = "PAID"
    db.commit()
    db.refresh(guide)

    return {"message": "Guia marcada como paga"}

@router.post(
    "/{guide_id}/pay",
    response_model=GuideOut,
)
def pay_guide_endpoint(
    guide_id: int,
    data: GuidePayRequest,
    db: Session = Depends(get_db),
):
    try:
        return pay_guide(
            db=db,
            guide_id=guide_id,
            paid_at=data.paid_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
