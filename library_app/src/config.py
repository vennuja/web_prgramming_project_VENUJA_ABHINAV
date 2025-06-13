from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from typing import List, Optional, Union
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "Library Management System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 jours

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000", "http://localhost:5500", "http://127.0.0.1:5500"]

    # Base de données
    DATABASE_URL: str = "sqlite:///./library.db"
    SQL_ECHO: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
