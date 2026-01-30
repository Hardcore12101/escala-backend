from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.database.session import SessionLocal
from src.app.database.seed import seed_system_company

router = APIRouter(prefix="/_internal", tags=["internal"])

@router.post("/bootstrap")
def bootstrap():
    db = SessionLocal()
    try:
        seed_system_company(db)
        return {"status": "ok"}
    finally:
        db.close()
