from fastapi import FastAPI
from app.core.config import settings
from app.routers import paypal

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    root_path=settings.API_V1_STR
)

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

app.include_router(paypal.auth_router)
app.include_router(paypal.product_router)
app.include_router(paypal.plan_router)
app.include_router(paypal.subscription_router)