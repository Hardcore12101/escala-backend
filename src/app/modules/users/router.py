from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.app.database.association_roles import user_company_role
from src.app.modules.permissions.enums import RoleEnum
from src.app.models.company import Company
from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.users.schemas import UserCreate, UserResponse, UserUpdate
from src.app.modules.users.service import create_user, update_user
from src.app.core.security import admin_only

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def read_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post("", response_model=UserResponse)
def create_new_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    return create_user(db, data, current_user)


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    return db.query(User).all()


@router.patch("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    try:
        return update_user(db, user_id, data, current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/make-admin/{user_id}")
def make_system_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    system_company = db.query(Company).filter(
        Company.name == "Escala Digital"
    ).first()

    if not system_company:
        raise HTTPException(status_code=500, detail="Empresa do sistema não existe")

    db.execute(
        user_company_role.insert().values(
            user_id=user_id,
            company_id=system_company.id,
            role=RoleEnum.ADMIN.value,
        )
    )
    db.commit()

    return {"ok": True}
    
    
@router.post("/companies/{company_id}/users")
def add_user(
    company_id: int,
    user_id: UUID,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    return add_user_to_company(
        db,
        user_id=user_id,
        company_id=company_id,
        role=role,
        admin_user=current_user,
    )
