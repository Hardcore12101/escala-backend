from decimal import Decimal
from pydantic import BaseModel


class ApurationCreate(BaseModel):
    company_id: int
    competence: str


class ApurationResponse(BaseModel):
    id: int
    company_id: int
    competence: str
    total_base: Decimal
    total_tax: Decimal
    status: str

    class Config:
        from_attributes = True
