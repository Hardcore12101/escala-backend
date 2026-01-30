from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # App
    APP_NAME: str = "Escala Digital"
    DEBUG: bool = False

    # Frontend
    VITE_API_URL: str = "http://localhost:5173"

    # API
    API_PREFIX: str = "/api"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",          # usado local
        env_ignore_empty=True,    # produção segura
        extra="forbid",
        case_sensitive=True,
    )


settings = AppSettings()
