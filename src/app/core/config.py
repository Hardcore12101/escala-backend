from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    # App
    app_name: str = "Escala Digital"
    debug: bool = True

    # API / Frontend
    vite_api_url: str = "http://localhost:5173"

    # Security
    SECRET_KEY: str = "Escalaadmin"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str

    class Config:
        env_file = BASE_DIR / ".env"
        extra = "forbid"  # explícito (boa prática)

settings = Settings()
