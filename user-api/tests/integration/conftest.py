import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from alembic import command
from alembic.config import Config
from app.config import settings


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    url = settings.SQLALCHEMY_DATABASE_URI
    url = str(url).replace("+asyncpg", "")
    create_engine(url)
    assert not database_exists(url), "Test database already exists. Aborting tests."
    create_database(url)
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    yield
    drop_database(url)
