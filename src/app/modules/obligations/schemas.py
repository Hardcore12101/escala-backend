from datetime import date
from pydantic import BaseModel
from app.modules.obligations.enums import ObligationType, ObligationStatus


class ObligationCreate(BaseModel):
    company_id: int
    type: ObligationType
    competence: str
    due_date: date


class ObligationResponse(BaseModel):
    id: int
    company_id: int
    type: ObligationType
    competence: str
    due_date: date
    status: ObligationStatus

    class Config:
        from_attributes = True
