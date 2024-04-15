import json
import os

from gutenberg.settings import SEARCH_CONFIGS_DIR


class EsIndex:
    def __init__(self, es_client, index_name):
        self.es_client = es_client
        self.index_name = index_name
        self.mappings = self.load_mappings()
        self.settings = self.load_settings()

    def load_mappings(self):
        """
        Retrieve mappings for this index from the search_configs/<index_name>.json file
        """
        if not os.path.exists(f'{SEARCH_CONFIGS_DIR}/{self.index_name}/mappings.json'):
            print(f'Mapping not defined at {SEARCH_CONFIGS_DIR}/{self.index_name}/mappings.json')
            return
        with open(f'{SEARCH_CONFIGS_DIR}/{self.index_name}/mappings.json') as f:
            return json.load(f)

    def load_settings(self):
        """
        Retrieve settings for this index from the search_configs/<index_name>.json file
        """
        if not os.path.exists(f'{SEARCH_CONFIGS_DIR}/{self.index_name}/settings.json'):
            print(f'Settings not defined at {SEARCH_CONFIGS_DIR}/{self.index_name}/settings.json')
            return
        with open(f'{SEARCH_CONFIGS_DIR}/{self.index_name}/settings.json') as f:
            return json.load(f)

    def create_index(self, force=False):
        if force and self.es_client.indices.exists(index=self.index_name):
            self.delete_index()
        self.es_client.indices.create(
            index=self.index_name,
            body={
                'mappings': self.mappings,
                'settings': self.settings
            })

    def delete_index(self):
        self.es_client.indices.delete(index=self.index_name)

    def index_document(self, document):
        assert '_id' in document, 'Document must have an _id field'
        es_id = document.pop('_id')
        self.es_client.index(
            index=self.index_name,
            id=es_id,
            body=document
        )

    def search(self, query):
        return self.es_client.search(index=self.index_name, body=query)
