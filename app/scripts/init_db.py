from app.core.db import Base, engine
from app.models.models import Product, Plan, Subscription

def init_db():
    print("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("All tables created.")

if __name__ == "__main__":
    init_db()