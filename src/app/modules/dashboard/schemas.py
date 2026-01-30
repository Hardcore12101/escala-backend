from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_apurations: int
    total_guides: int
    guides_paid: int
    guides_pending: int
    total_paid: float
    total_pending: float

class DashboardByCompetence(BaseModel):
    competence: str
    total_guides: int
    guides_paid: int
    guides_pending: int
    total_amount: float
    total_paid: float
    total_pending: float

class DashboardByTaxType(BaseModel):
    tax_type: str
    total_guides: int
    guides_paid: int
    guides_pending: int
    total_amount: float
    total_paid: float
    total_pending: float
