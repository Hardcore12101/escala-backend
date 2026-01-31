from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.app.database.association_roles import user_company_role
from src.app.modules.permissions.enums import RoleEnum
from src.app.models.company import Company
from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.users.schemas import UserCreate, UserResponse
from src.app.modules.users.service import create_user
from src.app.core.security import admin_only

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def read_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    # futuramente aqui entra controle de permissão (admin)
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    return create_user(
        db=db,
        email=data.email,
        password=data.password
    )

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