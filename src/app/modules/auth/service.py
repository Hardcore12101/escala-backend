from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.app.modules.users.service import get_user_by_email
from src.app.modules.auth.security import verify_password, create_access_token
from src.app.modules.audit.service import log_event


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    log_event(
        db,
        action="LOGIN",
        entity="user",
        entity_id=user.id,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
