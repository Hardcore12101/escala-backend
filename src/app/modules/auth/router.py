from fastapi import APIRouter, HTTPException, Depends
from src.app.core.security import create_access_token
from src.app.database.dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.app.modules.auth.service import authenticate_user
from src.app.modules.auth.schemas import Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}