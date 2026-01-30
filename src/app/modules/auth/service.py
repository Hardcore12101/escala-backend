from sqlalchemy.orm import Session
from src.app.modules.users.models import User
from src.app.modules.auth.security import verify_password, create_access_token
from src.app.modules.audit.service import log_event


def authenticate_user(db, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
