from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.modules.auth.security import verify_password, create_access_token
from app.modules.audit.service import log_event


def authenticate_user(db: Session, email: str, password: str) -> str | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    token = create_access_token({"sub": str(user.id)})

    log_event(
        db,
        action="LOGIN",
        entity="user",
        entity_id=user.id,
    )

    return token
