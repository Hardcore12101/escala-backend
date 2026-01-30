from pydantic import BaseModel
from typing import Optional


class CompanyBase(BaseModel):
    name: str
    cnpj: str


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    cnpj: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True
