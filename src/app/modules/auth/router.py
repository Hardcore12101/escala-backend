from fastapi import APIRouter, HTTPException, Depends
from src.app.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        email=form_data.username,  # username = email
        password=form_data.password,
    )
