import pytest
from elasticsearch import Elasticsearch

from app.config import settings
from app.orders.mappings import orders_mapping


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    elasticsearch = Elasticsearch(hosts=settings.ELASTICSEARCH_HOSTS)
    elasticsearch.indices.create(index="orders_test", mappings=orders_mapping)
    yield
    elasticsearch.indices.delete(index="orders_test")
