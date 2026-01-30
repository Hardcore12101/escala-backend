from fastapi import APIRouter, HTTPException
from src.app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(username: str, password: str):
    if username != "admin" or password != "admin":
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}
