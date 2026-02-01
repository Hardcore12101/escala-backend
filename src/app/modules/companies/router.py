from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.app.core.security import admin_only
from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.companies.schemas import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
)
from src.app.modules.companies.service import (
    create_company,
    list_companies,
    update_company,
    delete_company,
)

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    return create_company(db, data, current_user)


@router.get("")
def get_companies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sort: str = Query("name"),
    order: str = Query("asc"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list_companies(
        db=db,
        user=user,
        page=page,
        limit=limit,
        search=search,
        sort=sort,
        order=order,
    )


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company_route(
    company_id: int,
    data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    try:
        return update_company(db, company_id, data, current_user)
    except ValueError:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company_route(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    try:
        delete_company(db, company_id, current_user)
    except ValueError:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
