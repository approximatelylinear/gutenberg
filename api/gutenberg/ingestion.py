
import re

# Ingester
#   - Read a dataset
#   - Perform transformations
#   - Index the data

class Ingester:
    def __init__(self, client, dataset, es_index):
        self.client = client
        self.dataset = dataset
        self.es_index = es_index

    def ingest(self):
        data = self.read()
        data = self.transform(data)
        self.index(data)

    def read(self):
        raise NotImplementedError

    def transform(self, data):
        for transformer in self.transformers:
            data = transformer.transform(data)
        assert '_id' in data, 'Data must have an _id field'
        return data

    def index(self, data):
        self.client.index(index=self.es_index.name, id=data.pop('_id'), body=data)

    def add_transformer(self, transformer):
        self.transformers.append(transformer)


class GutenbergIngester(Ingester):
    def __init__(self, client, dataset, es_index):
        super().__init__(client, dataset, es_index)
        self.transformers = [GutenbergTransformer()]

    def read(self):
        return self.dataset.read()


class Transformer:
    def transform(self, data):
        raise NotImplementedError


class GutenbergTransformer(Transformer):
    def transform(self, data):
        result = {'_id': data['id']}
        metadata, text = re.split(
            r'\*\*\* ?START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK[^\*]+\*\*\*', data['text'], maxsplit=1)
        result['text'] = text.strip()
        kv_pattern = r"\n(?P<key>[\w ]+): (?P<value>[\w\d, \-.:;]+)?"
        meta_matches = re.findall(kv_pattern, metadata)
        if len(meta_matches) > 0:
            for key, value in meta_matches:
                if value is not None:
                    result[key.lower().replace(' ', '_')] = value.strip()
        result['metadata'] = metadata
        return result
