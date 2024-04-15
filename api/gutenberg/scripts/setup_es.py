
from gutenberg.client import make_client
from gutenberg.es_index import EsIndex
from gutenberg.ingestion import GutenbergIngester


def main():
    es_client = make_client()
    # Create gutenburg index
    gutenburg_index = EsIndex(
        es_client=es_client,
        index_name='gutenberg'
    )
    gutenburg_index.create_index(force=True)

    ingester = GutenbergIngester(
        es_index=gutenburg_index
    )
    ingester.ingest()


if __name__ == '__main__':
    main()
