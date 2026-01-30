from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.app.modules.users.models import User
from src.app.modules.users.service import get_user_by_email
from src.app.modules.auth.security import verify_password, create_access_token
from src.app.modules.audit.service import log_event


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user