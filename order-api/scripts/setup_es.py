from elasticsearch import Elasticsearch

from app.config import settings
from app.orders.mappings import orders_mapping

elasticsearch = Elasticsearch(hosts=settings.ELASTICSEARCH_HOSTS)

elasticsearch.indices.create(index="orders", mappings=orders_mapping)
