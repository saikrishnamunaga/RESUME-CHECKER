from __future__ import annotations
import os
from datetime import timedelta
from pathlib import Path
from typing import Set

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


class Config:
    """Base configuration for the Flask application."""

    SECRET_KEY: str = os.getenv('SECRET_KEY', 'please-change-this-secret')
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'DATABASE_URL', f"sqlite:///{BASE_DIR / 'ai_resume_analyzer.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False

    WTF_CSRF_ENABLED: bool = True
    WTF_CSRF_TIME_LIMIT = None

    UPLOAD_FOLDER: str = str(BASE_DIR / 'uploads')
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_CONTENT_LENGTH', 8 * 1024 * 1024))
    ALLOWED_EXTENSIONS: Set[str] = {'pdf', 'docx'}

    REPORTS_PER_PAGE: int = int(os.getenv('REPORTS_PER_PAGE', 10))
    PREFERRED_URL_SCHEME: str = os.getenv('PREFERRED_URL_SCHEME', 'https')
    DEBUG: bool = os.getenv('FLASK_DEBUG', '0') == '1'

    GOOGLE_OAUTH_CLIENT_ID: str = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
    GOOGLE_OAUTH_CLIENT_SECRET: str = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', '')
    FACEBOOK_OAUTH_CLIENT_ID: str = os.getenv('FACEBOOK_OAUTH_CLIENT_ID', '')
    FACEBOOK_OAUTH_CLIENT_SECRET: str = os.getenv('FACEBOOK_OAUTH_CLIENT_SECRET', '')


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SESSION_COOKIE_SECURE = True


def allowed_file(filename: str) -> bool:
    """Return True when the uploaded file has an allowed extension."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

__all__ = ['Config', 'DevelopmentConfig', 'ProductionConfig', 'config', 'allowed_file']
