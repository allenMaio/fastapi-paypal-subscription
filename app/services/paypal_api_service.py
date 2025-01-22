import requests
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from app.core.config import settings
from app.schemas.paypal_schema import (
    CreateProductRequest, CreatePlanRequest, CreateSubscriptionRequest,
    ShowSubscriptionDetailsQuery, ListTransactionsQuery,
    PatchOperation
)
from app.services.paypal_store import store_paypal_token

AUTH_BASE_URL = f"{settings.PAYPAL_BASE_URL}/oauth2/token"
PRODUCT_BASE_URL = f"{settings.PAYPAL_BASE_URL}/catalogs/products"
PLAN_BASE_URL = f"{settings.PAYPAL_BASE_URL}/billing/plans"
SUBSCRIPTION_BASE_URL = f"{settings.PAYPAL_BASE_URL}/billing/subscriptions"


def call_paypal_service(service_func, *args, **kwargs):
    try:
        return service_func(*args, **kwargs)
    except Exception as e:
        print(e)
        raise HTTPException(400, str(e))


# Auth
# ------------------------------------------------------------------------------
def generate_access_token(credentials: HTTPBasicCredentials) -> str:
    client_id = credentials.username or settings.PAYPAL_CLIENT_ID
    client_secret = credentials.password or settings.PAYPAL_CLIENT_SECRET
    if not client_id or not client_secret:
        raise ValueError("PayPal Client ID or Client Secret is missing.")
    
    url = AUTH_BASE_URL
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    response.raise_for_status()

    access_token = response.json().get("access_token")
    store_paypal_token(access_token)
    return {"message": "Access token generated successfully"}


# Product
# ------------------------------------------------------------------------------
def create_product(access_token: str, product: CreateProductRequest) -> dict:
    url = PRODUCT_BASE_URL
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers, json=product.model_dump())
    response.raise_for_status()
    res = response.json()
    res.pop("links", None)
    return res

def list_products(access_token: str) -> dict:
    url = PRODUCT_BASE_URL
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def show_product_details(access_token: str, product_id: str) -> dict:
    url = f"{PRODUCT_BASE_URL}/{product_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    res = response.json()
    res.pop("links", None)
    return res


# Plan
# ------------------------------------------------------------------------------
def create_plan(access_token: str, plan: CreatePlanRequest) -> dict:
    url = PLAN_BASE_URL
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers, json=plan.model_dump())
    response.raise_for_status()
    res = response.json()
    res.pop("links", None)
    return res

def list_plans(access_token: str) -> dict:
    url = PLAN_BASE_URL
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def show_plan_details(access_token: str, plan_id: str) -> dict:
    url = f"{PLAN_BASE_URL}/{plan_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    res = response.json()
    res.pop("links", None)
    return res


# Subscription
# ------------------------------------------------------------------------------
def create_subscription(access_token: str, subscription: CreateSubscriptionRequest) -> dict:
    url = SUBSCRIPTION_BASE_URL
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers, json=subscription.model_dump())
    response.raise_for_status()
    return response.json()

def show_subscription_details(access_token: str, subscription_id: str, query: ShowSubscriptionDetailsQuery) -> dict:
    url = f"{SUBSCRIPTION_BASE_URL}/{subscription_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {}
    if query:
        payload["fields"] = query.fields

    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    res = response.json()
    res.pop("links", None)
    res.pop("billing_info", None)
    return res

def update_subscription(access_token: str, subscription_id: str, data: list[PatchOperation]) -> dict:
    url = f"{SUBSCRIPTION_BASE_URL}/{subscription_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    dict_data = [op.model_dump() for op in data]

    response = requests.patch(url, headers=headers, json=dict_data)
    response.raise_for_status()
    if response.status_code == 204:
        return {"message": "Subscription updated successfully"}
    return response.json()

def list_transactions(access_token: str, subscription_id: str, query: ListTransactionsQuery) -> dict:
    url = f"{SUBSCRIPTION_BASE_URL}/{subscription_id}/transactions"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "start_time": query.start_time,
        "end_time": query.end_time
    }

    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()