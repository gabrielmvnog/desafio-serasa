from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.factories import create_user_out_data


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def user_id():
    return 1


@pytest.fixture
def mocked_create_user_service(mocker):
    return mocker.patch(
        "app.users.services.create_user", return_value=create_user_out_data()
    )


@pytest.fixture
def mocked_update_user_service(mocker):
    return mocker.patch("app.users.services.update_user", return_value=True)


@pytest.fixture
def mocked_delete_user_service(mocker):
    return mocker.patch("app.users.services.delete_user", return_value=True)


@pytest.fixture
def mocked_detail_user_service(mocker):
    return mocker.patch(
        "app.users.services.detail_user", return_value=create_user_out_data()
    )


@pytest.fixture
def mocked_list_users_service(mocker):
    return mocker.patch(
        "app.users.services.list_users", return_value=[create_user_out_data()]
    )


@pytest.fixture
def mocked_httpx_get(mocker):
    return mocker.patch(
        "httpx.AsyncClient.get", return_value=MagicMock(json=lambda: [])
    )
