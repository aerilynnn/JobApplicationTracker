from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# api/app/config.py -> parents[2] is the repo root, where .env lives
ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_ENV_FILE, extra="ignore")

    database_url: str

    cognito_region: str
    cognito_user_pool_id: str
    cognito_client_id: str

    @property
    def cognito_issuer(self) -> str:
        return (
            f"https://cognito-idp.{self.cognito_region}.amazonaws.com/{self.cognito_user_pool_id}"
        )

    @property
    def cognito_jwks_url(self) -> str:
        return f"{self.cognito_issuer}/.well-known/jwks.json"


settings = Settings()
