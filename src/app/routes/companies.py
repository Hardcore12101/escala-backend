from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyOut
from app.schemas.pagination import PaginatedResponse


router = APIRouter()

@router.get("/", response_model=PaginatedResponse[CompanyOut])
def list_companies(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=50),
    search: str | None = None,
    sort: str = "name",
    order: str = "asc",
    db: Session = Depends(get_db),
):
    query = db.query(Company)

    if search:
        query = query.filter(
            Company.name.ilike(f"%{search}%")
            | Company.cnpj.ilike(f"%{search}%")
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

@router.post("/", response_model=CompanyOut)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(**data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@router.put("/{company_id}", response_model=CompanyOut)
def update_company(company_id: int, data: CompanyUpdate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    for field, value in data.model_dump().items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company

@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(company)
    db.commit()
    return {"ok": True}
