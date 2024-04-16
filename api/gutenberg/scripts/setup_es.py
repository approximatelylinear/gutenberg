import argparse

from gutenberg.client import make_client
from gutenberg.es_index import EsIndex
from gutenberg.ingestion import GutenbergIngester
from gutenberg.search import Searcher

def main():
    # set up argument parser that takes in an index name and a command
    parser = argparse.ArgumentParser()
    parser.add_argument('index_name', help='Name of the index to create')

    # Optional command specifications. Can specify multiple commands
    parser.add_argument('--command', help='Command to execute',
                        nargs='+', default=[
                            'create_index', 'ingest', 'search'
                        ],
                        dest='commands')

    args = parser.parse_args()

    index_name = args.index_name
    commands = args.commands

    es_client = make_client()

    # Create gutenburg index
    gutenburg_index = EsIndex(
        es_client=es_client,
        index_name=index_name
    )
    if 'create_index' in commands:
        gutenburg_index.create_index(force=True)

    if 'ingest' in commands:
        ingester = GutenbergIngester(
            es_index=gutenburg_index
        )
        ingester.ingest()

    if 'search' in commands:
        searcher = Searcher(
            es_index=gutenburg_index
        )
        # print(searcher.all_docs())
        searcher.search("the", explain=True)


if __name__ == '__main__':
    main()
