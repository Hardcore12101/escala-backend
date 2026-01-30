from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.modules.dashboard.service import get_dashboard_summary
from app.modules.dashboard.schemas import DashboardSummary
from app.modules.dashboard.schemas import DashboardByCompetence
from app.modules.dashboard.service import get_dashboard_by_competence
from app.modules.dashboard.schemas import DashboardByTaxType
from app.modules.dashboard.service import get_dashboard_by_tax_type
from app.modules.auth.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return {
        "user_id": user.id,
        "email": user.email,
    }
    
@router.get("/summary/{company_id}", response_model=DashboardSummary)
def summary(company_id: int, db: Session = Depends(get_db)):
    return get_dashboard_summary(db, company_id)

@router.get(
    "/competence/{company_id}/{competence}",
    response_model=DashboardByCompetence,
)
def dashboard_competence(
    company_id: int,
    competence: str,
    db: Session = Depends(get_db),
):
    return get_dashboard_by_competence(db, company_id, competence)
    

@router.get(
    "/tax-type/{company_id}",
    response_model=list[DashboardByTaxType],
)
def dashboard_by_tax_type(
    company_id: int,
    db: Session = Depends(get_db),
):
    return get_dashboard_by_tax_type(db, company_id)