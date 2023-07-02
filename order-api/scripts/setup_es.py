from elasticsearch import BadRequestError, Elasticsearch
from loguru import logger

from app.config import settings
from app.orders.mappings import orders_mapping

elasticsearch = Elasticsearch(hosts=settings.ELASTICSEARCH_HOSTS)

try:
    elasticsearch.indices.create(index="orders", mappings=orders_mapping)
except BadRequestError:
    logger.warning("Resource already exists")
