from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.tax_rules.schemas import TaxRuleCreate, TaxRuleResponse
from src.app.modules.tax_rules.service import create_tax_rule
from src.app.core.security import admin_only

router = APIRouter(prefix="/tax-rules", tags=["Tax Rules"])


@router.post(
    "",
    response_model=TaxRuleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_rule(
    data: TaxRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    # futuramente: verificar se é admin do sistema
    return create_tax_rule(
        db=db,
        tax_type=data.tax_type,
        percentage=data.percentage,
        valid_from=data.valid_from,
    )
