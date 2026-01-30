from fastapi import APIRouter, Depends
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.core.deps import get_current_context

router = APIRouter(prefix="/me", tags=["Me"])

@router.get("/context")
def get_me_context(context=Depends(get_current_context)):
    return {
        "user": {
            "id": context["user"].id,
            "email": context["user"].email,
        },
        "company": {
            "id": context["company_id"],
        },
        "role": context["role"],
    }
