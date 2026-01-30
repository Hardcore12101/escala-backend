from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.tax_calculations.schemas import (
    TaxCalculationCreate,
    TaxCalculationResponse,
)
from src.app.modules.tax_calculations.service import calculate_tax

router = APIRouter(
    prefix="/tax-calculations",
    tags=["Tax Calculations"]
)


@router.post(
    "",
    response_model=TaxCalculationResponse,
    status_code=status.HTTP_201_CREATED,
)
def calculate(
    data: TaxCalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return calculate_tax(
        db=db,
        obligation_id=data.obligation_id,
        tax_type=data.tax_type,
        base_amount=data.base_amount,
    )
