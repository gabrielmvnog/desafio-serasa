import pytest
from fastapi.testclient import TestClient

from app.main import app
from tests.factories import create_user_out_data


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mocked_create_user_service(mocker):
    return mocker.patch("app.services.create_user", return_value=create_user_out_data())


@pytest.fixture
def mocked_update_user_service(mocker):
    return mocker.patch("app.services.update_user", return_value=create_user_out_data())


@pytest.fixture
def mocked_delete_user_service(mocker):
    return mocker.patch("app.services.delete_user", return_value=True)


@pytest.fixture
def mocked_detail_user_service(mocker):
    return mocker.patch("app.services.detail_user", return_value=create_user_out_data())


@pytest.fixture
def mocked_list_users_service(mocker):
    return mocker.patch("app.services.list_users", return_value=[create_user_out_data()])
