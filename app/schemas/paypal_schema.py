from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    name: str
    type: str
    id: str | None = None
    description: str | None = None
    category: str | None = None
    image_url: str | None = None
    home_url: str | None = None

class CreatePlanRequest(BaseModel):
    product_id: str
    name: str
    billing_cycles: list
    payment_preferences: dict
    status: str | None = "ACTIVE"
    description: str | None = None
    quantity_supported: bool | None = False
    taxes: dict | None = None

class CreateSubscriptionRequest(BaseModel):
    plan_id: str
    quantity: str | None = None
    auto_renewal: bool | None = False
    custom_id: str | None = None
    start_time: str | None = None
    shipping_amount: dict | None = None
    subscriber: dict | None = None
    application_context: dict | None = None
    plan: dict | None = None

class ShowSubscriptionDetailsQuery(BaseModel):
    fields: str | None = None

class ListTransactionsQuery(BaseModel):
    start_time: str
    end_time: str

class PatchOperation(BaseModel):
    op: str
    path: str
    value: dict