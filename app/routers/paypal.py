from fastapi import APIRouter, Depends ,HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas.product import Product
from app.services.paypal_service import generate_access_token, create_product, list_products, show_product_details
from app.services.paypal_store import store_paypal_token, get_paypal_token

security = HTTPBasic()

auth_router = APIRouter(tags=["auth"], prefix="/auth")

@auth_router.post("/login")
async def generate_access_token_route(
    credentials: HTTPBasicCredentials = Depends(security)
):
    try:
        client_id = credentials.username
        client_secret = credentials.password
        access_token = generate_access_token(client_id, client_secret)
        store_paypal_token(access_token)
        return {"message": "Access token generated successfully"}
    except Exception as e:
        raise HTTPException(400, str(e))


product_router = APIRouter(tags=["product"], prefix="/products")

@product_router.post("")
async def create_product_route(
    product: Product,
    access_token: str = Depends(get_paypal_token)
):
    try:
        return create_product(access_token, product)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

@product_router.get("")
async def list_products_route(
    access_token: str = Depends(get_paypal_token)
):
    try:
        return list_products(access_token)
    except Exception as e:
        print(e)

@product_router.get("/{product_id}")
async def show_product_details_route(
    product_id: str,
    access_token: str = Depends(get_paypal_token)
):
    try:
        return show_product_details(access_token, product_id)
    except Exception as e:
        print(e)