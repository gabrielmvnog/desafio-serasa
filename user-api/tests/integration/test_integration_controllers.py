from fastapi import status

from tests.factories import create_user_in_data


async def test_integration_create_should_return_user(client, create_url):
    response = await client.put(create_url, json=create_user_in_data())
    content = response.json()
    content.pop("created_at")

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "User Test",
        "cpf": "21238906001",
        "email": "user_test@gmail.com",
        "phone_number": "+5521999999999",
        "id": 1,
        "updated_at": None,
    }


async def test_integration_create_should_return_see_other(client, create_url):
    response = await client.put(
        create_url, json=create_user_in_data(), follow_redirects=False
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.content == b""


async def test_integration_create_should_return_unprocessable_entity(
    client, create_url
):
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


async def test_integration_detail_should_return_user(client, detail_url):
    response = await client.get(detail_url)
    content = response.json()
    content.pop("created_at")

    assert content == {
        "name": "User Test",
        "cpf": "21238906001",
        "email": "user_test@gmail.com",
        "phone_number": "+5521999999999",
        "id": 1,
        "updated_at": None,
    }


async def test_integration_detail_should_return_not_found(client):
    response = await client.get("/users/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


async def test_integration_list_should_return_users(client, list_url):
    response = await client.get(list_url)
    content = response.json()
    content[0].pop("created_at")

    assert response.status_code == status.HTTP_200_OK
    assert content == [
        {
            "name": "User Test",
            "cpf": "21238906001",
            "email": "user_test@gmail.com",
            "phone_number": "+5521999999999",
            "id": 1,
            "updated_at": None,
        }
    ]


async def test_integration_update_should_return_updated_user(client, update_url):
    response = await client.post(update_url, json=create_user_in_data())

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


async def test_integration_update_should_return_unprocessable_entity(
    client, update_url
):
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


async def test_integration_update_should_return_not_found(client):
    response = await client.post("/users/2", json=create_user_in_data())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


async def test_integration_delete_should_return_no_content(client, delete_url):
    response = await client.delete(delete_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


async def test_integration_delete_should_return_not_found(client):
    response = await client.delete("/users/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


async def test_integration_delete_should_return_conflict(client):
    response = await client.delete("/users/99999")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "User id [99999] has orders"}


async def test_integration_list_should_return_empty_list(client, list_url):
    response = await client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
