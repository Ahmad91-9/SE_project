import os
from pathlib import Path


class Config:
    """Default Flask configuration."""

    APP_NAME = "Ventixe Event Management"
    SECRET_KEY = os.environ.get("VENTIXE_SECRET_KEY", "dev-secret-change-me")

    BASE_DIR = Path(__file__).resolve().parent.parent
    INSTANCE_DIR = Path(os.environ.get("VENTIXE_INSTANCE_DIR", BASE_DIR / "instance"))
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get(
            "VENTIXE_DATABASE_URI", f"sqlite:///{(INSTANCE_DIR / 'ventixe.db').as_posix()}"
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("VENTIXE_COOKIE_SECURE", "0") == "1"

