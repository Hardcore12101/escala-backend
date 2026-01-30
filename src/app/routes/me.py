from fastapi import APIRouter, Depends
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.core.deps import get_current_context

router = APIRouter(prefix="/me", tags=["Me"])

@router.get("")
def me(ctx: CurrentContext = Depends(get_current_context)):
    return {
        "user": ctx.user.email,
        "company": ctx.company.name,
        "role": ctx.role,
    }