
from functools import cache

from elasticsearch import Elasticsearch

from gutenberg.settings import CERT_PATH, ELASTIC_PASSWORD, ELASTIC_USER, ELASTIC_URL


@cache
def make_client():
    print(f'Creating Elasticsearch client with url: {ELASTIC_URL}')
    print(f'Using cert path: {CERT_PATH}')
    return Elasticsearch(
        ELASTIC_URL,
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        verify_certs=True,
        ca_certs=CERT_PATH,
    )

