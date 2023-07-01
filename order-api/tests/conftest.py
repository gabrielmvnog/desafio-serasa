from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.orders.schemas import OrderIn, OrderOut
from tests.factories import create_order_in_data, create_order_out_data


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def order_in_data():
    return OrderIn(**create_order_in_data())


@pytest.fixture
def order_out_data():
    return OrderOut(**create_order_out_data())


@pytest.fixture
def mocked_create_order_service(mocker, order_out_data):
    return mocker.patch("app.orders.services.create_order", return_value=order_out_data)


@pytest.fixture
def mocked_update_order_service(mocker):
    return mocker.patch("app.orders.services.update_order", return_value=True)


@pytest.fixture
def mocked_delete_order_service(mocker):
    return mocker.patch("app.orders.services.delete_order", return_value=True)


@pytest.fixture
def mocked_detail_order_service(mocker, order_out_data):
    return mocker.patch("app.orders.services.detail_order", return_value=order_out_data)


@pytest.fixture
def mocked_list_orders_service(mocker, order_out_data):
    return mocker.patch(
        "app.orders.services.list_orders", return_value=[order_out_data]
    )


@pytest.fixture
def mocked_httpx_get(mocker):
    return mocker.patch(
        "httpx.AsyncClient.get", return_value=MagicMock(status_code=200)
    )
