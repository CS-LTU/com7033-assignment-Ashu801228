import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    # Secret key for sessions & CSRF protection
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a-very-secure-secret-key"

    # Default database (used for authentication / users)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "instance" / "auth.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Second database (used for patient records)
    SQLALCHEMY_BINDS = {
        "patients": "sqlite:///" + str(BASE_DIR / "instance" / "patients.db"),
    }

    # ----------------------------
    # Secure Session Configuration
    # ----------------------------
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    # In real HTTPS deployment you could also enable:
    # SESSION_COOKIE_SECURE = True
    # REMEMBER_COOKIE_SECURE = True
