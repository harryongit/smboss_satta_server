from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel
import os


load_dotenv()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "SMBoss")
    app_env: str = os.getenv("APP_ENV", "development")
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", 8000))
    jwt_secret: str = os.getenv("JWT_SECRET", "change_me")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    class Config:
        arbitrary_types_allowed = True


@lru_cache
def get_settings() -> Settings:
    return Settings()

