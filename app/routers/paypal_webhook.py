from fastapi import APIRouter, Request
from app.services.paypal_webhook_service import webhook_handler

webhook_router = APIRouter(tags=["webhook"], prefix="/webhooks")

@webhook_router.post("")
async def webhook_route(
    request: Request
):
    return await webhook_handler(request)