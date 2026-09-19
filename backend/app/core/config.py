"""
Python Mastery - Application Configuration
Reads environment variables for Supabase, OpenAI, Runner timeouts, and CORS.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Python Mastery API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # CORS configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "*"
    ]

    # Supabase (PostgreSQL + Auth)
    SUPABASE_URL: str = "https://your-project.supabase.co"
    SUPABASE_ANON_KEY: str = "your-anon-key"
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/postgres"

    # AI Mentor (OpenAI API via backend)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Runner Sandbox Settings
    RUNNER_TIMEOUT_SECONDS: float = 3.0
    RUNNER_MAX_MEMORY_MB: int = 64

    # Security & JWT Auth
    JWT_SECRET_KEY: str = "super-secret-production-python-mastery-jwt-key-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
