from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.app.core.security import get_db
from sqlalchemy import text

router = APIRouter(prefix="/health", tags=["Health"])

@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def health_check():
    return {"status": "ok"}

@router.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    db.execute("SELECT 1")
    return {"ok": True}
