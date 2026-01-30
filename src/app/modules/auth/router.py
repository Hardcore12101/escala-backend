from fastapi import APIRouter, HTTPException, Depends
from src.app.core.security import create_access_token, get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.app.modules.auth.service import authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
    }