
import itertools
import json
import os
import re

from pprint import pformat
from jinja2 import Template

from gutenberg.settings import SEARCH_CONFIGS_DIR


def extract_per_field_similarity(explanation):
    result = []

    def dfs(node):
        if "description" in node and "PerFieldSimilarity" in node["description"]:
            # Extract field, term, and weight
            parts = node["description"].split("weight(")[1].split(")")[0].split(":")
            field = parts[0]
            term = re.sub(r' in \d+', '', parts[1])
            weight = node["value"]

            # Add to result dictionary
            result.append({
                "field": field,
                "term": term,
                "weight": round(weight, 2)
            })

        # Recursively traverse details
        if "details" in node:
            for detail in node["details"]:
                dfs(detail)

    dfs(explanation)
    # throw out the all but the max weight for each field

    # use itertools groupby to group by field and term, then
    # use max to get the max weight for each group
    result = sorted(result, key=lambda x: x["term"])
    result = list(reversed(sorted([max(g, key=lambda x: x['weight']) for k, g in itertools.groupby(result, key=lambda x: x["term"])], key=lambda x: x["weight"])))
    return result


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

    # def explain_doc(self, doc_id):

    def search(self,
               query,
               page_number=1,
               highlight=False,
               size=10,
               explain=False):
        # Render the template with the query string
        es_query = json.loads(self.query_template.render(qs=query))
        if explain:
            es_query['explain'] = True
        result = self.es_client.search(
            index=self.index_name,
            **es_query
        )
        result = self.es_client.search(index=self.index_name,**es_query)
        # print(pformat(result))
        # import pdb; pdb.set_trace()
        hits = result['hits']['hits']
        if explain:
            for hit in hits:
                hit['parsed_explanation'] = extract_per_field_similarity(hit['_explanation'])
        hits = [hit for hit in hits]
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

    @classmethod
    def get_indices(self):
        search_configs = os.listdir(SEARCH_CONFIGS_DIR)
        indices = [index for index in search_configs if os.path.isdir(os.path.join(SEARCH_CONFIGS_DIR, index))]
        return [{'name': index, 'id': index} for index in indices]
