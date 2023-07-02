import pytest
from fastapi import status

from app.users.exceptions import ConflictException, UserNotFounException
from tests.factories import create_user_in_data


@pytest.mark.usefixtures("mocked_create_user_service")
async def test_unit_create_should_return_user(client, create_url):
    response = await client.put(create_url, json=create_user_in_data())

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "name": "User Test",
        "cpf": "21238906001",
        "email": "user_test@gmail.com",
        "phone_number": "+5521999999999",
        "id": 1,
        "created_at": "2023-07-01T00:00:00",
        "updated_at": "2023-07-01T00:00:00",
    }


async def test_unit_create_should_return_unprocessable_entity(client, create_url):
    response = await client.put(create_url, json={"not": "ok"})

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
            {
                "loc": ["body", "not"],
                "msg": "extra fields not permitted",
                "type": "value_error.extra",
            },
        ]
    }


async def test_unit_create_should_return_see_other(
    client, create_url, mocked_create_user_service
):
    mocked_create_user_service.side_effect = ConflictException
    response = await client.put(
        create_url, json=create_user_in_data(), follow_redirects=False
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.content == b""


@pytest.mark.usefixtures("mocked_update_user_service")
async def test_unit_update_should_return_updated_user(client, update_url):
    response = await client.post(update_url, json=create_user_in_data())

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


async def test_unit_update_should_return_unprocessable_entity(client, update_url):
    response = await client.post(update_url, json={"not": "ok"})

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
            {
                "loc": ["body", "not"],
                "msg": "extra fields not permitted",
                "type": "value_error.extra",
            },
        ]
    }


async def test_unit_update_should_return_not_found(
    client, update_url, mocked_update_user_service
):
    mocked_update_user_service.return_value = False
    response = await client.post(update_url, json=create_user_in_data())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


@pytest.mark.usefixtures("mocked_delete_user_service", "mocked_httpx_get")
async def test_unit_delete_should_return_no_content(client, delete_url):
    response = await client.delete(delete_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


@pytest.mark.usefixtures("mocked_httpx_get")
async def test_unit_delete_should_return_not_found(
    client, delete_url, mocked_delete_user_service
):
    mocked_delete_user_service.return_value = False
    response = await client.delete(delete_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


@pytest.mark.usefixtures("mocked_detail_user_service")
async def test_unit_detail_should_return_user(client, detail_url):
    response = await client.get(detail_url)

    assert response.json() == {
        "name": "User Test",
        "cpf": "21238906001",
        "email": "user_test@gmail.com",
        "phone_number": "+5521999999999",
        "id": 1,
        "created_at": "2023-07-01T00:00:00",
        "updated_at": "2023-07-01T00:00:00",
    }


async def test_unit_detail_should_return_not_found(
    client, detail_url, mocked_detail_user_service
):
    mocked_detail_user_service.side_effect = UserNotFounException
    response = await client.get(detail_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


@pytest.mark.usefixtures("mocked_list_users_service")
async def test_unit_list_should_return_users(client, list_url):
    response = await client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "name": "User Test",
            "cpf": "21238906001",
            "email": "user_test@gmail.com",
            "phone_number": "+5521999999999",
            "id": 1,
            "created_at": "2023-07-01T00:00:00",
            "updated_at": "2023-07-01T00:00:00",
        }
    ]


async def test_unit_list_should_return_empty_list(
    client, list_url, mocked_list_users_service
):
    mocked_list_users_service.return_value = []
    response = await client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
