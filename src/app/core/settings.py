from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "development"

settings = Settings()
