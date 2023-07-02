import asyncio
from unittest import mock
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from app.orders.schemas import OrderIn, OrderOut
from tests.factories import create_order_in_data, create_order_out_data

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    from app.main import app

    async with AsyncClient(
        app=app,
        base_url="http://app",
        headers={"Authorization": "Bearer hardcoded-token"},
    ) as client:
        yield client


@pytest.fixture
def create_url():
    return "/orders/1"


@pytest.fixture
def update_url():
    return "/orders/1"


@pytest.fixture
def delete_url():
    return "/orders/1"


@pytest.fixture
def list_url():
    return "/orders"


@pytest.fixture
def detail_url():
    return "/orders/1"


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
