from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from app.modules.companies.schemas import CompanyCreate, CompanyResponse
from app.modules.companies.service import create_company

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_company(
        db,
        name=data.name,
        cnpj=data.cnpj,
        user=current_user
    )
