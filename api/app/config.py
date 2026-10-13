from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# api/app/config.py -> parents[2] is the repo root, where .env lives
ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_ENV_FILE, extra="ignore")

    database_url: str


settings = Settings()
