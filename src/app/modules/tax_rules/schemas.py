from datetime import date
from pydantic import BaseModel


class TaxRuleCreate(BaseModel):
    tax_type: str
    percentage: float
    valid_from: date


class TaxRuleResponse(BaseModel):
    id: int
    tax_type: str
    percentage: float
    valid_from: date
    valid_to: date | None

    class Config:
        from_attributes = True
