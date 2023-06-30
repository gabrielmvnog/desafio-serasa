import pytest
from fastapi import status


@pytest.fixture
def ping_url():
    return "/ping"


def test_unit_create_should_return_user(client, ping_url):
    response = client.get(ping_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
