from typing import Optional

from pydantic import BaseSettings, EmailStr
from decouple import config


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 days

    JWT_SECRET: str = config("JWT_SECRET")
    JWT_ALGORITHM = config("JWT_ALGORITHM")

    API_V1_STR: str = "/api/v1"
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    class Config:
        case_sensitive = True


settings = Settings()
