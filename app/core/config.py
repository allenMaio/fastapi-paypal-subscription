import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    PROJECT_NAME: str = "fastapi-paypal-subscription"
    API_V1_STR: str = "/api/v1"

    PAYPAL_BASE_URL: str = "https://api-m.sandbox.paypal.com/v1"
    PAYPAL_CLIENT_ID: str
    PAYPAL_CLIENT_SECRET: str
    PAYPAL_WEBHOOK_ID: str

    DB: str = "postgresql"
    DB_NAME: str = "paypal_test"
    DB_USER: str = "myuser"
    DB_PASSWORD: str
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = "5432"

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()