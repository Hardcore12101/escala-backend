from fastapi import APIRouter, Depends
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User

router = APIRouter(prefix="/me", tags=["Me"])


@router.get("")
def read_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
