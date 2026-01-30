from sqlalchemy.orm import Session
from src.app.modules.users.models import User
from src.app.modules.auth.security import hash_password
from src.app.modules.audit.service import log_event


def create_user(db: Session, email: str, password: str) -> User:
    user = User(
        email=email,
        hashed_password=hash_password(password),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    log_event(
        db,
        action="CREATE_USER",
        entity="user",
        entity_id=user.id,
    )

    return user
