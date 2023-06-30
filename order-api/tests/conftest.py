import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.factories import create_order_out_data


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mocked_create_order_service(mocker):
    return mocker.patch(
        "app.services.create_order", return_value=create_order_out_data()
    )


@pytest.fixture
def mocked_update_order_service(mocker):
    return mocker.patch("app.services.update_order", return_value=True)


@pytest.fixture
def mocked_delete_order_service(mocker):
    return mocker.patch("app.services.delete_order", return_value=True)


@pytest.fixture
def mocked_detail_order_service(mocker):
    return mocker.patch(
        "app.services.detail_order", return_value=create_order_out_data()
    )


@pytest.fixture
def mocked_list_orders_service(mocker):
    return mocker.patch(
        "app.services.list_orders", return_value=[create_order_out_data()]
    )
