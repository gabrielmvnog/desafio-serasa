from unittest.mock import AsyncMock, MagicMock

import pytest
from elasticsearch import ConflictError, NotFoundError

from app.orders.exceptions import ConflictException, OrderNotFounException
from app.orders.schemas import OrderOut
from app.orders.services import (
    create_order,
    delete_order,
    detail_order,
    list_orders,
    update_order,
)


async def test_create_order_should_create(order_in_data):
    order = await create_order(AsyncMock(), order_in=order_in_data, order_id=1)

    assert isinstance(order, OrderOut)


async def test_create_order_should_raise_conflict(order_in_data):
    with pytest.raises(ConflictException):
        await create_order(
            AsyncMock(
                create=MagicMock(
                    side_effect=ConflictError(meta=MagicMock(), message="", body={})
                )
            ),
            order_in=order_in_data,
            order_id=1,
        )


async def test_update_order_should_update(order_in_data):
    result = await update_order(AsyncMock(), order_in=order_in_data, order_id=1)

    assert result is True


async def test_update_order_should_raise_not_found(order_in_data):
    with pytest.raises(OrderNotFounException):
        await update_order(
            AsyncMock(
                update=MagicMock(
                    side_effect=NotFoundError(meta=MagicMock(), message="", body={})
                )
            ),
            order_in=order_in_data,
            order_id=1,
        )


async def test_delete_order_should_delete():
    result = await delete_order(AsyncMock(), order_id=1)

    assert result is True


async def test_delete_order_should_raise_not_found():
    with pytest.raises(OrderNotFounException):
        await delete_order(
            AsyncMock(
                delete=MagicMock(
                    side_effect=NotFoundError(meta=MagicMock(), message="", body={})
                )
            ),
            order_id=1,
        )


async def test_get_order_should_return_order(order_out_data):
    result = await detail_order(
        AsyncMock(
            get=AsyncMock(
                return_value={
                    "_id": order_out_data.id,
                    "_source": order_out_data.dict(exclude={"id"}),
                }
            )
        ),
        order_id=1,
    )

    assert result == order_out_data.dict()


async def test_get_order_should_raise_not_found():
    with pytest.raises(OrderNotFounException):
        await detail_order(
            AsyncMock(
                get=MagicMock(
                    side_effect=NotFoundError(meta=MagicMock(), message="", body={})
                )
            ),
            order_id=1,
        )


async def test_list_orders_should_return_orders(order_out_data):
    result = await list_orders(
        AsyncMock(
            search=AsyncMock(
                return_value={
                    "hits": {
                        "hits": [
                            {
                                "_id": order_out_data.id,
                                "_source": order_out_data.dict(exclude={"id"}),
                            }
                        ]
                    }
                }
            )
        )
    )

    assert result == [order_out_data.dict()]


async def test_delete_order_should_raise_conflict():
    result = await list_orders(
        AsyncMock(search=AsyncMock(return_value={"hits": {"hits": []}}))
    )

    assert result == []
