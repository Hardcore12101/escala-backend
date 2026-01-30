from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.apurations.schemas import ApurationCreate, ApurationResponse
from app.modules.apurations.service import close_month

router = APIRouter(prefix="/apurations", tags=["Apurations"])


@router.post(
    "/close",
    response_model=ApurationResponse,
    status_code=status.HTTP_201_CREATED,
)
def close(
    data: ApurationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return close_month(
        db=db,
        company_id=data.company_id,
        competence=data.competence,
    )

@router.get("/company/{company_id}")
def list_apurations(
    company_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Apuration)
        .filter(Apuration.company_id == company_id)
        .order_by(Apuration.competence.desc())
        .all()
    )
