from fastapi import APIRouter, Depends
from src.app.core.deps import get_current_user

router = APIRouter(prefix="/me", tags=["me"])

@router.get("/")
def read_me(user: str = Depends(get_current_user)):
    return {
        "username": user
    }
