from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy import String, Text, JSON, BOOLEAN
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from app.core.db import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_id: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(127))
    type: Mapped[str] = mapped_column(String(30))
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    home_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_time: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    updated_time: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    plans: Mapped[List["Plan"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, unique_id={self.unique_id!r}, name={self.name!r}, type={self.type!r})"

class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    unique_id: Mapped[str] = mapped_column(String(30))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    name: Mapped[str] = mapped_column(String(127))
    billing_cycles: Mapped[list[dict]] = mapped_column(JSON)
    payment_preferences: Mapped[dict] = mapped_column(JSON)
    status: Mapped[Optional[str]] = mapped_column(String(30), nullable=False, default="ACTIVE")
    description: Mapped[Optional[str]] = mapped_column(String(127), nullable=True)
    quantity_supported: Mapped[Optional[bool]] = mapped_column(BOOLEAN, nullable=False, default=False)
    taxes: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_time: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    updated_time: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    product: Mapped["Product"] = relationship(back_populates="plans")

    subscriptions: Mapped[List["Subscription"]] = relationship(
        back_populates="plan",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Plan(id={self.id!r}, unique_id={self.unique_id!r}, product_id={self.product_id!r}, name={self.name!r})"

class Subscription(Base):
    
    __tablename__ = "subscriptions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    unique_id: Mapped[str] = mapped_column(String(30))
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"))
    quantity: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    auto_renewal: Mapped[Optional[bool]] = mapped_column(BOOLEAN, nullable=False, default=False)
    custom_id: Mapped[Optional[str]] = mapped_column(String(127), nullable=True)
    start_time: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    shipping_amount: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    subscriber: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    application_context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    created_time: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    updated_time: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    plan: Mapped["Plan"] = relationship(back_populates="subscriptions")

    def __repr__(self) -> str:
        return f"Subscription(id={self.id!r}, unique_id={self.unique_id!r}, plan_id={self.plan_id!r})"