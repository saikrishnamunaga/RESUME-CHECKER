from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./db.sqlite3"
    SECRET_KEY: str = "super-secret-dev-key-change-in-production"
    GOOGLE_CLIENT_ID: str = "dummy-google-client-id-for-dev"
    GOOGLE_CLIENT_SECRET: str = "dummy-google-client-secret-for-dev"
    FRONTEND_URL: str = "http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500,http://localhost:5173"
    PROJECT_NAME: str = "Resume Screening"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = Settings()


