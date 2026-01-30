from decimal import Decimal
from pydantic import BaseModel


class TaxCalculationCreate(BaseModel):
    obligation_id: int
    tax_type: str
    base_amount: Decimal


class TaxCalculationResponse(BaseModel):
    id: int
    obligation_id: int
    base_amount: Decimal
    percentage: Decimal
    tax_amount: Decimal

    class Config:
        from_attributes = True
