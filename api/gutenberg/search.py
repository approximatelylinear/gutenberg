
import os
from jinja2 import Template

from gutenberg.settings import SEARCH_CONFIGS_DIR


class Searcher:
    def __init__(self, es_index):
        self.es_index = es_index
        self.es_client = es_index.es_client
        self.index_name = es_index.index_name
        self.query_template = self.load_query_template()

    def load_query_template(self):
        path = f'{SEARCH_CONFIGS_DIR}/{self.index_name}/search.jinja'
        if not os.path.exists(path):
            print(f'Search template not defined at {path}')
            return
        with open(path, "r") as f:
            return Template(f.read())

    def search(self, query):
        # Render the template with the query string
        es_query = self.query_template.render(qs=query)
        result = self.es_client.search(
            index=self.index_name,
            body=es_query
        )
        hits = result['hits']['hits']
        return hits
