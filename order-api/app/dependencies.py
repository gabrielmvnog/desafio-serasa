from typing import Generator

from app.db.session import SessionLocal
from app.orders.schemas import OrderIn


def validate_order(order_in: OrderIn):
    return order_in


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
