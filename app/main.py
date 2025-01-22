from fastapi import FastAPI
from app.core.config import settings
from app.routers import paypal_api, paypal_webhook

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    root_path=settings.API_V1_STR
)

app.include_router(paypal_api.auth_router)
app.include_router(paypal_api.product_router)
app.include_router(paypal_api.plan_router)
app.include_router(paypal_api.subscription_router)
app.include_router(paypal_webhook.webhook_router)