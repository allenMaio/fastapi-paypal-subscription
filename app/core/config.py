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

settings = Settings()