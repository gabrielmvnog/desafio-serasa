from sqlalchemy.orm import Session

from app.schemas import OrderIn, OrderOut


def list_orders(db: Session, skip: int = 0, limit: int = 10) -> list[OrderOut | None]:
    ...


def detail_order(db: Session, order_id: int) -> OrderOut:
    ...


def create_order(db: Session, order_in: OrderIn, order_id: int) -> OrderOut:
    ...


def update_order(db: Session, order_in: OrderIn, order_id: int) -> bool:
    ...


def delete_order(db: Session, order_id: int) -> bool:
    ...
