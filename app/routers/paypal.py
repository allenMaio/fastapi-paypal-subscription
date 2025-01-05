from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas.product import Product
from app.services.paypal_service import call_paypal_service, generate_access_token, create_product, list_products, show_product_details
from app.services.paypal_store import get_paypal_token

security = HTTPBasic()

auth_router = APIRouter(tags=["auth"], prefix="/auth")

@auth_router.post("/login")
async def generate_access_token_route(
    credentials: HTTPBasicCredentials = Depends(security)
):
    return call_paypal_service(generate_access_token, credentials)


product_router = APIRouter(tags=["product"], prefix="/products")

@product_router.post("")
async def create_product_route(
    product: Product,
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(create_product, access_token, product)

@product_router.get("")
async def list_products_route(
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(list_products, access_token)

@product_router.get("/{product_id}")
async def show_product_details_route(
    product_id: str,
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(show_product_details, access_token, product_id)