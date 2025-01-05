import requests
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from app.core.config import settings
from app.schemas.product import Product
from app.services.paypal_store import store_paypal_token


def call_paypal_service(service_func, *args, **kwargs):
    try:
        return service_func(*args, **kwargs)
    except Exception as e:
        print(e)
        raise HTTPException(400, str(e))

def generate_access_token(credentials: HTTPBasicCredentials) -> str:
    client_id = credentials.username or settings.PAYPAL_CLIENT_ID
    client_secret = credentials.password or settings.PAYPAL_CLIENT_SECRET
    if not client_id or not client_secret:
        raise ValueError("PayPal Client ID or Client Secret is missing.")
    
    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    response.raise_for_status()

    access_token = response.json().get("access_token")
    store_paypal_token(access_token)
    return {"message": "Access token generated successfully"}

def create_product(access_token: str, product: Product) -> dict:
    url = f"{settings.PAYPAL_BASE_URL}/v1/catalogs/products"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers, json=product.model_dump())
    response.raise_for_status()
    return response.json()

def list_products(access_token: str) -> dict:
    url = f"{settings.PAYPAL_BASE_URL}/v1/catalogs/products"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def show_product_details(access_token: str, product_id: str) -> dict:
    url = f"{settings.PAYPAL_BASE_URL}/v1/catalogs/products/{product_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()