from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.models import Product, Plan, Subscription


# Product
# ------------------------------------------------------------------------------
def create_product(
        db: Session,
        unique_id: str,
        name: str,
        type_: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        image_url: Optional[str] = None,
        home_url: Optional[str] = None
) -> Product:
    product = Product(
        unique_id=unique_id,
        name=name,
        type=type_,
        description=description,
        category=category,
        image_url=image_url,
        home_url=home_url
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def get_product_by_id(
        db: Session,
        product_id: int
) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_unique_id(
        db: Session,
        unique_id: str
) -> Optional[Product]:
    return db.query(Product).filter(Product.unique_id == unique_id).first()

def update_product(
        db: Session,
        product_id: int,
        **kwargs
) -> Optional[Product]:
    item = get_product_by_id(db, product_id)
    if not item:
        return None
    for key, value in kwargs.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_product(
        db: Session,
        product_id: int
) -> bool:
    item = get_product_by_id(db, product_id)
    if item:
        db.delete(item)
        db.commit()
        return True
    return False


# Plan
# ------------------------------------------------------------------------------
def create_plan(
        db: Session,
        unique_id: str,
        product_id: int,
        name: str,
        billing_cycles: list[dict],
        payment_preferences: dict,
        status: Optional[str] = "ACTIVE",
        **kwargs
) -> Plan:
    plan = Plan(
        unique_id=unique_id,
        product_id=product_id,
        name=name,
        billing_cycles=billing_cycles,
        payment_preferences=payment_preferences,
        status=status,
        **kwargs
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

def get_plans(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[Plan]:
    return db.query(Plan).offset(skip).limit(limit).all()

def get_plan_by_id(
        db: Session,
        plan_id: int
) -> Optional[Plan]:
    return db.query(Plan).filter(Plan.id == plan_id).first()

def get_plan_by_unique_id(
        db: Session,
        unique_id: str
) -> Optional[Plan]:
    return db.query(Plan).filter(Plan.unique_id == unique_id).first()


# Subscription
# ------------------------------------------------------------------------------
def create_subscription(
        db: Session,
        unique_id: str,
        plan_id: int,
        **kwargs
) -> Subscription:
    subscription = Subscription(
        unique_id=unique_id,
        plan_id=plan_id,
        **kwargs
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

def get_subscriptions(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[Subscription]:
    return db.query(Subscription).offset(skip).limit(limit).all()

def get_subscription_by_id(
        db: Session,
        subscription_id: int
) -> Optional[Subscription]:
    return db.query(Subscription).filter(Subscription.id == subscription_id).first()

def get_subscription_by_unique_id(
        db: Session,
        unique_id: str
) -> Optional[Subscription]:
    return db.query(Subscription).filter(Subscription.unique_id == unique_id).first()

def update_subscription(
        db: Session,
        subscription_id: int,
        **kwargs
) -> Optional[Subscription]:
    item = get_subscription_by_id(db, subscription_id)
    if not item:
        return None
    for key, value in kwargs.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item