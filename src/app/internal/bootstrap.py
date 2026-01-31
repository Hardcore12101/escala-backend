from fastapi import APIRouter, Header, HTTPException
from sqlalchemy.orm import Session

from src.app.database.session import SessionLocal
from src.app.modules.users.models import User
from src.app.core.security import get_password_hash
from src.app.core.config import settings

router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("/bootstrap")
def bootstrap_admin(x_bootstrap_secret: str = Header(...)):
    if x_bootstrap_secret != settings.BOOTSTRAP_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()

        if user:
            return {"status": "admin already exists"}

        admin = User(
            email=settings.ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            is_active=True,
            is_admin=True,
        )

        db.add(admin)
        db.commit()

        return {"status": "admin created"}
    finally:
        db.close()
