import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    PROPAGATE_EXCEPTIONS = True

    API_TITLE = "OMS REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    # Use DB_URL from .env, or default to data/db.sqlite3 in project root
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL", f"sqlite:///db.sqlite3")

    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 900
    JWT_REFRESH_TOKEN_EXPIRES = 86400
    JWT_TOKEN_LOCATION = ['headers']

    @staticmethod
    def validate():
        if not Config.JWT_SECRET_KEY:
            raise RuntimeError("SECRET_KEY missing")
        if not Config.SQLALCHEMY_DATABASE_URI:
            raise RuntimeError("DB_URL missing")

