import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str
    app_env: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int


@lru_cache
def get_settings() -> Settings:
    load_dotenv(override=False)
    return Settings(
        app_name=os.getenv("APP_NAME", "Movie Ticket Booking API"),
        app_env=os.getenv("APP_ENV", "development"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./movie_booking.db"),
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", "change-me-before-running-outside-localhost"),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
    )
