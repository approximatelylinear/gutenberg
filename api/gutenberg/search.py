
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

    def search(self, query, page_number=1, highlight=False, size=10):
        # Render the template with the query string
        es_query = self.query_template.render(qs=query)
        result = self.es_client.search(
            index=self.index_name,
            body=es_query
        )
        hits = result['hits']['hits']
        # return just the title
        hits = [{'title': hit['_source']['title']} for hit in hits]
        return hits

    def random_doc(self):
        result = self.es_client.search(
            index=self.index_name,
            body={
                "query": {
                    "function_score": {
                        "random_score": {}}
                        }, "size": 1}
        )
        return result['hits']['hits'][0]['_source']

    def all_docs(self):
        result = self.es_client.search(
            index=self.index_name,
            body={"query": {"match_all": {}}}
        )
        return result['hits']['hits']
