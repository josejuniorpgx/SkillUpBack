from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Settings class for application configuration.

    This class includes various configuration settings for the Leadership Feedback
    Survey API application. It covers database connection details, server
    configuration, application-specific settings, CORS origins, security settings,
    and"""

    DATABASE_URL: str = "sqlite:///./leadership_survey.db"

    PORT: int = 8000
    HOST: str = "0.0.0.0"

    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    FRONTEND_URL: str = "http://localhost:3000"

    APP_TITLE: str = "Leadership Feedback Survey API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API for collecting anonymous leadership feedback from team members"

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Leadership Feedback Survey"

    SECRET_KEY: str = "your-super-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
