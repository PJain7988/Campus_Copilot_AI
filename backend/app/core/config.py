import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CampusCopilot AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-key-change-in-production-campus-copilot"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./campuscopilot.db"
    USE_SQLITE_FALLBACK: bool = True
    
    # Gemini
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-1.5-pro"
    GEMINI_EMBEDDING_MODEL: str = "text-embedding-004"
    
    # Institution Info
    DEFAULT_UNIVERSITY_CODE: str = "GU"
    DEFAULT_UNIVERSITY_NAME: str = "Geeta University, Panipat"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
