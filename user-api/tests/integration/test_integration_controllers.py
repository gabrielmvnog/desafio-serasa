import pytest
from fastapi import status

from tests.factories import create_user_in_data


@pytest.fixture
def create_url():
    return "/users/1"


@pytest.fixture
def update_url():
    return "/users/1"


@pytest.fixture
def delete_url():
    return "/users/1"


@pytest.fixture
def list_url():
    return "/users"


@pytest.fixture
def detail_url():
    return "/users/1"


def test_integration_create_should_return_user(client, create_url):
    response = client.put(create_url, json=create_user_in_data().dict())
    content = response.json()
    content.pop("created_at")

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "User Test",
        "cpf": "212.389.060-01",
        "email": "user_test@gmail.com",
        "phone_number": "(61)995637801",
        "id": 1,
        "updated_at": None,
    }


def test_integration_create_should_return_see_other(client, create_url):
    response = client.put(
        create_url, json=create_user_in_data().dict(), follow_redirects=False
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.content == b""


def test_integration_create_should_return_unprocessable_entity(client, create_url):
    response = client.put(create_url, json={"not": "ok"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "cpf"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "phone_number"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_integration_detail_should_return_user(client, detail_url):
    response = client.get(detail_url)
    content = response.json()
    content.pop("created_at")

    assert content == {
        "name": "User Test",
        "cpf": "212.389.060-01",
        "email": "user_test@gmail.com",
        "phone_number": "(61)995637801",
        "id": 1,
        "updated_at": None,
    }


def test_integration_detail_should_return_not_found(client):
    response = client.get("/users/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_integration_list_should_return_users(client, list_url):
    response = client.get(list_url)
    content = response.json()
    content[0].pop("created_at")

    assert response.status_code == status.HTTP_200_OK
    assert content == [
        {
            "name": "User Test",
            "cpf": "212.389.060-01",
            "email": "user_test@gmail.com",
            "phone_number": "(61)995637801",
            "id": 1,
            "updated_at": None,
        }
    ]


def test_integration_update_should_return_updated_user(client, update_url):
    response = client.post(update_url, json=create_user_in_data().dict())

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b"null"


def test_integration_update_should_return_unprocessable_entity(client, update_url):
    response = client.post(update_url, json={"not": "ok"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "cpf"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "phone_number"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_integration_update_should_return_not_found(client):
    response = client.post("/users/2", json=create_user_in_data().dict())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


@pytest.mark.usefixtures("mocked_httpx_get")
def test_integration_delete_should_return_no_content(client, delete_url):
    response = client.delete(delete_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


@pytest.mark.usefixtures("mocked_httpx_get")
def test_integration_delete_should_return_not_found(client):
    response = client.delete("/users/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_integration_list_should_return_empty_list(client, list_url):
    response = client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
