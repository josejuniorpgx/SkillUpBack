from typing import List
from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = config("API_V1_STR", default="/api/v1")
    PROJECT_NAME: str = config("PROJECT_NAME", default="Leadership Feedback Survey")

    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./leadership_survey.db")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Environment
    ENVIRONMENT: str = config("ENVIRONMENT", default="development")

    # Server
    HOST: str = config("HOST", default="0.0.0.0")
    PORT: int = config("PORT", default=8000, cast=int)

    # Security (para futuras features)
    SECRET_KEY: str = config("SECRET_KEY", default="your-super-secret-key-change-in-production")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)

    class Config:
        case_sensitive = True


# Global settings instance
settings = Settings()
