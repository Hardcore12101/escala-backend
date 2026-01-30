from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.obligations.schemas import (
    ObligationCreate,
    ObligationResponse,
)
from app.modules.obligations.service import create_obligation

router = APIRouter(prefix="/obligations", tags=["Obligations"])


@router.post(
    "",
    response_model=ObligationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_obligation(
    data: ObligationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_obligation(
        db=db,
        company_id=data.company_id,
        type=data.type,
        competence=data.competence,
        due_date=data.due_date,
    )
