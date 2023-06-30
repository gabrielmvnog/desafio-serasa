from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.orders.exceptions import ConflictException, OrderNotFounException
from app.orders.models import Order
from app.orders.schemas import OrderIn, OrderOut


def list_orders(db: Session, skip: int = 0, limit: int = 10) -> list[OrderOut | None]:
    return db.query(Order).offset(skip).limit(limit).all()


def detail_order(db: Session, order_id: int) -> OrderOut:
    try:
        db_order = db.query(Order).filter(Order.id == order_id).one()
    except NoResultFound:
        raise OrderNotFounException from None

    return OrderOut.from_orm(db_order)


def create_order(db: Session, order_in: OrderIn, order_id: int) -> OrderOut:
    order_in_data = jsonable_encoder(order_in)
    db_order = Order(id=order_id, **order_in_data)

    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    except IntegrityError as err:
        if "UniqueViolation" in err.args[0]:
            raise ConflictException from None

    return OrderOut.from_orm(db_order)


def update_order(db: Session, order_in: OrderIn, order_id: int) -> bool:
    order_in_data = jsonable_encoder(order_in)
    updated = db.query(Order).filter(Order.id == order_id).update(order_in_data)
    db.commit()

    return bool(updated)


def delete_order(db: Session, order_id: int) -> bool:
    deleted = db.query(Order).filter(Order.id == order_id).delete()
    db.commit()

    return bool(deleted)
