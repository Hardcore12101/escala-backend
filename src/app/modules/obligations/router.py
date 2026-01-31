from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.obligations.schemas import (
    ObligationCreate,
    ObligationResponse,
)
from src.app.modules.obligations.service import create_obligation
from src.app.core.security import admin_only

router = APIRouter(prefix="/obligations", tags=["Obligations"])


@router.post(
    "",
    response_model=ObligationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_obligation(
    data: ObligationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    return create_obligation(
        db=db,
        company_id=data.company_id,
        type=data.type,
        competence=data.competence,
        due_date=data.due_date,
    )
