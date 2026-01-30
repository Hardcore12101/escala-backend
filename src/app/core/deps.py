from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.app.database.session import SessionLocal
from src.app.database.association_roles import user_company_role
from src.app.modules.users.models import User
from src.app.core.security import get_current_user, get_db
from src.app.models.company import Company
from src.app.core.context import CurrentContext



def get_current_context(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    company_id: int = Header(..., alias="X-Company-Id"),
) -> CurrentContext:

    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    link = (
        db.query(user_company_role)
        .filter(
            user_company_role.c.user_id == user.id,
            user_company_role.c.company_id == company.id,
            user_company_role.c.is_active == True,
        )
        .first()
    )

    if not link:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não pertence à empresa",
        )

    return CurrentContext(
        user=user,
        company=company,
        role=link.role,
    )