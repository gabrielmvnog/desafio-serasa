import logging
from datetime import datetime

from elasticsearch import AsyncElasticsearch, ConflictError, NotFoundError

from app.config import settings
from app.orders.exceptions import ConflictException, OrderNotFounException
from app.orders.schemas import OrderIn, OrderOut

logger = logging.getLogger(__name__)


async def list_orders(
    db: AsyncElasticsearch, user_id: int | None = None, skip: int = 0, limit: int = 10
) -> list[OrderOut | None]:
    query = None

    if user_id:
        query = {"match": {"user_id": user_id}}

    results = await db.search(
        index=settings.ORDERS_INDEX,
        query=query,
        from_=skip,
        size=limit,
    )

    return [{"id": hits["_id"], **hits["_source"]} for hits in results["hits"]["hits"]]


async def detail_order(db: AsyncElasticsearch, order_id: int) -> OrderOut:
    try:
        db_order = await db.get(index=settings.ORDERS_INDEX, id=order_id)
    except NotFoundError:
        raise OrderNotFounException from None

    return {"id": db_order["_id"], **db_order["_source"]}


async def create_order(
    db: AsyncElasticsearch, order_in: OrderIn, order_id: int
) -> OrderOut:
    order_out = OrderOut(id=order_id, **order_in.dict())

    try:
        await db.create(
            index=settings.ORDERS_INDEX,
            id=order_id,
            document=order_out.dict(exclude={"id"}),
        )
    except ConflictError:
        raise ConflictException from None

    return order_out


async def update_order(
    db: AsyncElasticsearch, order_in: OrderIn, order_id: int
) -> bool:
    order_out = OrderOut(id=order_id, updated_at=datetime.utcnow(), **order_in.dict())

    try:
        updated = await db.update(
            index=settings.ORDERS_INDEX,
            id=order_id,
            doc=order_out.dict(exclude={"id", "created_at"}),
        )
    except NotFoundError:
        raise OrderNotFounException from None

    return bool(updated)


async def delete_order(db: AsyncElasticsearch, order_id: int) -> bool:
    try:
        deleted = await db.delete(index=settings.ORDERS_INDEX, id=order_id)
    except NotFoundError:
        raise OrderNotFounException from None

    return bool(deleted)
