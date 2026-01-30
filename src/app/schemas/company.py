from pydantic import BaseModel, Field
from typing import Optional

class CompanyBase(BaseModel):
    name: str = Field(min_length=3)
    cnpj: str = Field(min_length=14, max_length=14)

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3)

class CompanyOut(CompanyBase):
    id: int

    class Config:
        from_attributes = True

class CompanyListOut(BaseModel):
    items: list[CompanyOut]
    total: int