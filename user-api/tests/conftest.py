import asyncio
from unittest import mock
from unittest.mock import MagicMock

import pytest
from fastapi import status
from httpx import AsyncClient

from app.users.schemas import UserOut
from tests.factories import create_user_out_data

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
def user_id():
    return 1


@pytest.fixture
def create_url(user_id):
    return f"/users/{user_id}"


@pytest.fixture
def update_url(user_id):
    return f"/users/{user_id}"


@pytest.fixture
def delete_url(user_id):
    return f"/users/{user_id}"


@pytest.fixture
def detail_url(user_id):
    return f"/users/{user_id}"


@pytest.fixture
def list_url():
    return "/users"


@pytest.fixture
def user_out_data():
    return UserOut.parse_obj(create_user_out_data())


@pytest.fixture
def mocked_create_user_service(mocker, user_out_data):
    return mocker.patch("app.users.services.create_user", return_value=user_out_data)


@pytest.fixture
def mocked_update_user_service(mocker):
    return mocker.patch("app.users.services.update_user", return_value=True)


@pytest.fixture
def mocked_delete_user_service(mocker):
    return mocker.patch("app.users.services.delete_user", return_value=True)


@pytest.fixture
def mocked_detail_user_service(mocker, user_out_data):
    return mocker.patch("app.users.services.detail_user", return_value=user_out_data)


@pytest.fixture
def mocked_list_users_service(mocker, user_out_data):
    return mocker.patch("app.users.services.list_users", return_value=[user_out_data])


@pytest.fixture
def mocked_httpx_get(mocker):
    return mocker.patch(
        "httpx.AsyncClient.get",
        return_value=MagicMock(json=lambda: [], status_code=status.HTTP_200_OK),
    )
