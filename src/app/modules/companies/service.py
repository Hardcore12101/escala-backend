from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID
from src.app.models.company import Company
from src.app.modules.users.models import User
from src.app.modules.audit.service import log_event
from src.app.modules.companies.schemas import CompanyCreate, CompanyUpdate


def create_company(
    db: Session,
    data: CompanyCreate,
    user: User
) -> Company:
    company = Company(
        name=data.name,
        cnpj=data.cnpj,
    )

    company.users.append(user)

    db.add(company)
    db.commit()
    db.refresh(company)

    log_event(
        db,
        action="CREATE_COMPANY",
        user_id=str(user.id),
        entity="company",
        entity_id=company.id,
    )

    return company


def list_companies(
    db: Session,
    user: User,
    page: int,
    limit: int,
    search: str | None,
    sort: str,
    order: str,
):
    query = (
        db.query(Company)
        .join(Company.users)
        .filter(User.id == user.id)
    )

    if search:
        query = query.filter(
            or_(
                Company.name.ilike(f"%{search}%"),
                Company.cnpj.ilike(f"%{search}%"),
            )
        )

    total = query.count()

    sort_col = Company.name if sort == "name" else Company.cnpj
    if order == "desc":
        sort_col = sort_col.desc()

    items = (
        query
        .order_by(sort_col)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": items,
        "total": total,
    }


def update_company(
    db: Session,
    company_id: int,
    data: CompanyUpdate,
    user: User,
) -> Company:
    company = (
        db.query(Company)
        .join(Company.users)
        .filter(Company.id == company_id, User.id == user.id)
        .first()
    )

    if not company:
        raise ValueError("Empresa não encontrada")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)

    log_event(
        db,
        action="UPDATE_COMPANY",
        user_id=str(user.id),
        entity="company",
        entity_id=company.id,
    )

    return company


def delete_company(
    db: Session,
    company_id: int,
    user: User,
):
    company = (
        db.query(Company)
        .join(Company.users)
        .filter(Company.id == company_id, User.id == user.id)
        .first()
    )

    if not company:
        raise ValueError("Empresa não encontrada")

    db.delete(company)
    db.commit()

    log_event(
        db,
        action="DELETE_COMPANY",
        user_id=str(user.id),
        entity="company",
        entity_id=company_id,
    )


def add_user_to_company(
    *,
    db: Session,
    current_user: User,
    target_user_id: UUID,
    company_id: UUID,
    role: str,
):
    # 1️⃣ Verifica se a empresa existe
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    # 2️⃣ Verifica se o usuário alvo existe
    target_user = db.query(User).filter(User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 3️⃣ Evita vínculo duplicado
    if target_user in company.users:
        raise HTTPException(
            status_code=400,
            detail="Usuário já vinculado à empresa",
        )

    # 4️⃣ Faz o vínculo
    company.users.append(target_user)
    db.commit()

    # 5️⃣ Auditoria (obrigatória no seu projeto)
    log_event(
        db=db,
        action="ADD_USER_TO_COMPANY",
        user_id=str(current_user.id),
        entity="company",
        entity_id=str(company_id),
        extra={
            "target_user_id": str(target_user_id),
            "role": role,
        },
    )