import pytest
from fastapi import status

from app.orders.exceptions import ConflictException, OrderNotFounException
from tests.factories import create_order_in_data


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


@pytest.mark.usefixtures("mocked_create_order_service", "mocked_httpx_get")
def test_unit_create_should_return_order(client, create_url):
    response = client.put(create_url, json=create_order_in_data())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "user_id": 1,
        "item_description": "Iphone 14",
        "item_quantity": 10,
        "item_price": 15000,
        "total_value": 150000,
        "id": 1,
        "created_at": "2023-07-01T00:00:00",
        "updated_at": "2023-07-01T00:00:00",
    }


def test_unit_create_should_return_unprocessable_entity(client, create_url):
    response = client.put(create_url, json={"not": "ok"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "user_id"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "item_description"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "item_quantity"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "item_price"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "total_value"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "not"],
                "msg": "extra fields not permitted",
                "type": "value_error.extra",
            },
            {
                "loc": ["body", "__root__"],
                "msg": "unsupported operand type(s) for *: 'NoneType' and 'NoneType'",
                "type": "type_error",
            },
        ]
    }


@pytest.mark.usefixtures("mocked_httpx_get")
def test_unit_create_should_return_see_other(
    client, create_url, mocked_create_order_service
):
    mocked_create_order_service.side_effect = ConflictException
    response = client.put(
        create_url, json=create_order_in_data(), follow_redirects=False
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.content == b""


@pytest.mark.usefixtures("mocked_update_order_service")
def test_unit_update_should_return_updated_order(client, update_url):
    response = client.post(update_url, json=create_order_in_data())

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b"null"


def test_unit_update_should_return_unprocessable_entity(client, update_url):
    response = client.post(update_url, json={"not": "ok"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "user_id"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "item_description"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "item_quantity"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "item_price"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "total_value"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "not"],
                "msg": "extra fields not permitted",
                "type": "value_error.extra",
            },
            {
                "loc": ["body", "__root__"],
                "msg": "unsupported operand type(s) for *: 'NoneType' and 'NoneType'",
                "type": "type_error",
            },
        ]
    }


def test_unit_update_should_return_not_found(
    client, update_url, mocked_update_order_service
):
    mocked_update_order_service.return_value = False
    response = client.post(update_url, json=create_order_in_data())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


@pytest.mark.usefixtures("mocked_delete_order_service")
def test_unit_delete_should_return_no_content(client, delete_url):
    response = client.delete(delete_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


def test_unit_delete_should_return_not_found(
    client, delete_url, mocked_delete_order_service
):
    mocked_delete_order_service.return_value = False
    response = client.delete(delete_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


@pytest.mark.usefixtures("mocked_detail_order_service")
def test_unit_detail_should_return_order(client, detail_url):
    response = client.get(detail_url)

    assert response.json() == {
        "user_id": 1,
        "item_description": "Iphone 14",
        "item_quantity": 10,
        "item_price": 15000,
        "total_value": 150000,
        "id": 1,
        "created_at": "2023-07-01T00:00:00",
        "updated_at": "2023-07-01T00:00:00",
    }


def test_unit_detail_should_return_not_found(
    client, detail_url, mocked_detail_order_service
):
    mocked_detail_order_service.side_effect = OrderNotFounException
    response = client.get(detail_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


@pytest.mark.usefixtures("mocked_list_orders_service")
def test_unit_list_should_return_orders(client, list_url):
    response = client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "user_id": 1,
            "item_description": "Iphone 14",
            "item_quantity": 10,
            "item_price": 15000,
            "total_value": 150000,
            "id": 1,
            "created_at": "2023-07-01T00:00:00",
            "updated_at": "2023-07-01T00:00:00",
        }
    ]


def test_unit_list_should_return_empty_list(
    client, list_url, mocked_list_orders_service
):
    mocked_list_orders_service.return_value = []
    response = client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
