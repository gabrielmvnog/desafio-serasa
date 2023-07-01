import pytest

from app.orders.schemas import OrderIn
from tests.factories import create_order_in_data


@pytest.mark.parametrize(
    "value",
    [
        {"item_quantity": 1, "item_price": 10.00, "total_value": 10.00},
        {"item_quantity": 2, "item_price": 10.00, "total_value": 20.00},
        {"item_quantity": 2, "item_price": 15.00, "total_value": 30.00},
    ],
)
def test_schema_order_in_should_accept_valid_total_value(value):
    order = create_order_in_data()
    order.update(**value)

    order_in = OrderIn.parse_obj(order)

    assert isinstance(order_in, OrderIn)
    assert order_in.total_value == value["total_value"]


@pytest.mark.parametrize(
    "value",
    [
        {"item_quantity": 1, "item_price": 10.00, "total_value": 15.00},
        {"item_quantity": 2, "item_price": 10.00, "total_value": 40.00},
        {"item_quantity": 2, "item_price": 15.00, "total_value": 60.00},
    ],
)
def test_schema_order_in_should_raise_for_total_value(value):
    order = create_order_in_data()
    order.update(**value)

    with pytest.raises(ValueError):
        OrderIn.parse_obj(order)


def test_schema_order_in_should_raise_for_zero_item_quantity():
    order = create_order_in_data()
    order["item_quantity"] = 0

    with pytest.raises(ValueError):
        OrderIn.parse_obj(order)
