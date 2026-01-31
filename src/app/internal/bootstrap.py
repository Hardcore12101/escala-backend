from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.app.core.database import get_db
from src.app.core.security import get_password_hash
from src.app.modules.users.models import User
from src.app.core.config import settings

router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("/bootstrap")
def bootstrap_admin(
    secret: str,
    db: Session = Depends(get_db),
):
    if secret != settings.BOOTSTRAP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bootstrap secret",
        )

    admin_exists = db.query(User).filter(User.role == "admin").first()
    if admin_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin already exists",
        )

    hashed_password = get_password_hash(settings.ADMIN_PASSWORD)

    admin_user = User(
        email=settings.ADMIN_EMAIL,
        hashed_password=hashed_password,
        role="admin",
        is_active=True,
    )

    try:
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin already exists or database constraint error",
        )

    return {"message": "Admin created successfully"}
