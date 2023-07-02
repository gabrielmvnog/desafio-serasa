from asyncio import sleep

from fastapi import status

from tests.factories import create_order_in_data


async def test_integration_create_should_return_order(client, create_url):
    response = await client.put(create_url, json=create_order_in_data())
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


async def test_integration_list_should_return_orders(client, list_url):
    await sleep(1)
    response = await client.get(list_url)

    content = response.json()
    content[0].pop("created_at")

    assert response.status_code == status.HTTP_200_OK
    assert content == [
        {
            "user_id": 1,
            "item_description": "Iphone 14",
            "item_quantity": 10,
            "item_price": 15000.0,
            "total_value": 150000.0,
            "id": 1,
            "updated_at": None,
        }
    ]


async def test_integration_create_should_return_see_other(client, create_url):
    response = await client.put(
        create_url, json=create_order_in_data(), follow_redirects=False
    )

    assert response.status_code == status.HTTP_303_SEE_OTHER
    assert response.content == b""


async def test_integration_detail_should_return_order(client, detail_url):
    response = await client.get(detail_url)
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


async def test_integration_detail_should_return_not_found(client):
    response = await client.get("/orders/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


async def test_integration_update_should_return_updated_order(client, update_url):
    response = await client.post(update_url, json=create_order_in_data())

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


async def test_integration_update_should_return_not_found(client):
    response = await client.post("/orders/2", json=create_order_in_data())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


async def test_integration_delete_should_return_no_content(client, delete_url):
    response = await client.delete(delete_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""


async def test_integration_delete_should_return_not_found(client):
    response = await client.delete("/orders/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Order not found"}


async def test_integration_list_should_return_empty_list(client, list_url):
    await sleep(1)
    response = await client.get(list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
