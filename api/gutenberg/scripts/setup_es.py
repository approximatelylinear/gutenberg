
from gutenberg.client import make_client
from gutenberg.es_index import EsIndex

def main():
    es_client = make_client()
    # Create gutenburg index
    gutenburg_index = EsIndex(
        es_client=es_client,
        index_name='gutenberg'
    )
    gutenburg_index.create_index(force=True)


if __name__ == '__main__':
    main()
