from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.app.database.session import SessionLocal
from src.app.database.association_roles import user_company_role
from src.app.modules.users.models import User
from src.app.core.security import get_current_user, get_db


def get_current_context(
    company_id: int = Header(..., alias="X-Company-Id"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = db.execute(
        user_company_role.select().where(
            (user_company_role.c.user_id == user.id)
            & (user_company_role.c.company_id == company_id)
        )
    ).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não possui acesso a esta empresa",
        )

    return {
        "user": user,
        "company_id": company_id,
        "role": result.role,
    }