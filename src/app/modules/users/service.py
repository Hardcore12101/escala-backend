from sqlalchemy.orm import Session
from src.app.modules.users.models import User
from src.app.modules.auth.security import hash_password
from src.app.modules.audit.service import log_event
from src.app.core.security import get_password_hash
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID

def create_user(db, data, admin_user):
    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role=data.role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    log_event(
        db,
        action="CREATE_USER",
        user_id=str(admin_user.id),
        entity="user",
        entity_id=user.id,
        metadata={"email": user.email, "role": user.role},
    )

    return user


def update_user(db, user_id, data, admin_user):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("Usuário não encontrado")

    if data.role is not None:
        user.role = data.role
    if data.is_active is not None:
        user.is_active = data.is_active

    db.commit()

    log_event(
        db,
        action="UPDATE_USER",
        user_id=str(admin_user.id),
        entity="user",
        entity_id=user.id,
        metadata={"role": user.role, "is_active": user.is_active},
    )

    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()
    
def add_user_to_company(
    db: Session,
    *,
    user_id: UUID,
    company_id: int,
    role: str,
    admin_user: User,
):
    link = UserCompany(
        user_id=user_id,
        company_id=company_id,
        role=role,
    )
    db.add(link)
    db.commit()

    log_event(
        db,
        action="ADD_USER_TO_COMPANY",
        user_id=str(admin_user.id),
        entity="company",
        entity_id=company_id,
        metadata={"user_id": str(user_id), "role": role},
    )

    return link

