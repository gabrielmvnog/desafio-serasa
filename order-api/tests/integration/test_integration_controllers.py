import pytest
from fastapi import status

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


def test_integration_create_should_return_order(client, create_url):
    response = client.put(create_url, json=create_order_in_data().dict())
    content = response.json()
    content.pop("created_at")

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "user_id": 1,
        "item_description": "Iphone 14",
        "item_quantity": 10,
        "item_price": 15000,
        "total_value": 150000,
        "id": 1,
        "updated_at": None,
    }


def test_integration_create_should_return_see_other(client, create_url):
    response = client.put(
        create_url, json=create_order_in_data().dict(), follow_redirects=False
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.content == b""


def test_integration_create_should_return_unprocessable_entity(client, create_url):
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
        ]
    }


def test_integration_detail_should_return_order(client, detail_url):
    response = client.get(detail_url)
    content = response.json()
    content.pop("created_at")

    assert content == {
        "user_id": 1,
        "item_description": "Iphone 14",
        "item_quantity": 10,
        "item_price": 15000,
        "total_value": 150000,
        "id": 1,
        "updated_at": None,
    }


def test_integration_detail_should_return_not_found(client):
    response = client.get("/orders/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


def test_integration_list_should_return_orders(client, list_url):
    response = client.get(list_url)
    content = response.json()
    content[0].pop("created_at")

    assert response.status_code == status.HTTP_200_OK
    assert content == [
        {
            "user_id": 1,
            "item_description": "Iphone 14",
            "item_quantity": 10,
            "item_price": 15000,
            "total_value": 150000,
            "id": 1,
            "updated_at": None,
        }
    ]


def test_integration_update_should_return_updated_order(client, update_url):
    response = client.post(update_url, json=create_order_in_data().dict())

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b"null"


def test_integration_update_should_return_unprocessable_entity(client, update_url):
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
        ]
    }


def test_integration_update_should_return_not_found(client):
    response = client.post("/orders/2", json=create_order_in_data().dict())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


def test_integration_delete_should_return_no_content(client, delete_url):
    response = client.delete(delete_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


def test_integration_delete_should_return_not_found(client):
    response = client.delete("/orders/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


def test_integration_list_should_return_empty_list(client, list_url):
    response = client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
