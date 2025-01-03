from fastapi import FastAPI
from app.core.config import settings
from app.routers import paypal

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

app.include_router(paypal.auth_router, prefix=settings.API_V1_STR)
app.include_router(paypal.product_router, prefix=settings.API_V1_STR)