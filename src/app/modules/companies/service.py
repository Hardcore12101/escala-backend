from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.app.models.company import Company
from src.app.modules.users.models import User
from src.app.modules.companies.schemas import CompanyCreate, CompanyUpdate


def create_company(db: Session, data: CompanyCreate, user: User) -> Company:
    company = Company(
        name=data.name,
        cnpj=data.cnpj,
        owner_id=user.id,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def list_companies(db: Session, user: User) -> list[Company]:
    return (
        db.query(Company)
        .filter(Company.owner_id == user.id)
        .all()
    )


def update_company(
    db: Session,
    company_id: int,
    data: CompanyUpdate,
    user: User,
) -> Company:
    company = (
        db.query(Company)
        .filter(
            Company.id == company_id,
            Company.owner_id == user.id,
        )
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company_id: int, user: User) -> None:
    company = (
        db.query(Company)
        .filter(
            Company.id == company_id,
            Company.owner_id == user.id,
        )
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(company)
    db.commit()
