from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas.paypal_schema import Product, Plan, Subscription
from app.services.paypal_service import (
    call_paypal_service,
    generate_access_token,
    create_product, list_products, show_product_details,
    create_plan, list_plans, show_plan_details,
    create_subscription, show_subscription_details, update_subscription 
)
from app.services.paypal_store import get_paypal_token

security = HTTPBasic()


# Auth
# ------------------------------------------------------------------------------
auth_router = APIRouter(tags=["auth"], prefix="/auth")

@auth_router.post("/login")
def generate_access_token_route(
    credentials: HTTPBasicCredentials = Depends(security)
):
    return call_paypal_service(generate_access_token, credentials)


# Product
# ------------------------------------------------------------------------------
product_router = APIRouter(tags=["product"], prefix="/products")

@product_router.post("")
def create_product_route(
    product: Product,
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(create_product, access_token, product)

@product_router.get("")
def list_products_route(
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(list_products, access_token)

@product_router.get("/{product_id}")
def show_product_details_route(
    product_id: str,
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(show_product_details, access_token, product_id)


# Plan
# ------------------------------------------------------------------------------
plan_router = APIRouter(tags=["plan"], prefix="/plans")

@plan_router.post("")
def create_plan_route(
    plan: Plan,
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(create_plan, access_token, plan)

@plan_router.get("")
def list_plans_route(
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(list_plans, access_token)

@plan_router.get("/{plan_id}")
def show_plan_details_route(
    plan_id: str,
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(show_plan_details, access_token, plan_id)


# Subscription
# ------------------------------------------------------------------------------
subscription_router = APIRouter(tags=["subscription"], prefix="/subscriptions")

@subscription_router.post("")
def create_subscription_route(
    subscription: Subscription,
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(create_subscription, access_token, subscription)

@subscription_router.get("/{subscription_id}")
def show_subscription_details_route(
    subscription_id: str,
    fields: str = None,
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(show_subscription_details, access_token, subscription_id, fields)

@subscription_router.patch("/{subscription_id}")
def update_subscription_route(
    subscription_id: str,
    data: list[dict],
    access_token: str = Depends(get_paypal_token)
):
    return call_paypal_service(update_subscription, access_token, subscription_id, data)