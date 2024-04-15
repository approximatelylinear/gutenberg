
import re

from datasets import load_dataset


class Ingester:
    def __init__(self, es_index):
        self.es_index = es_index
        self.transformers = []

    def ingest(self):
        data = self.read()
        data = self.transform(data)
        self.index(data)

    def read(self):
        raise NotImplementedError

    def transform(self, data):
        for transformer in self.transformers:
            data = transformer.transform(data)
        return data

    def index(self, data):
        if isinstance(data, dict):
            self.es_index.index_document(data)
        else:
            for doc in data:
                self.es_index.index_document(doc)

    def add_transformer(self, transformer):
        self.transformers.append(transformer)


class GutenbergIngester(Ingester):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_transformer(GutenbergTransformer())

    def read(self):
        gutenberg_ds = load_dataset(
            'manu/project_gutenberg',
            split="en[:1%]"
        )
        for row in gutenberg_ds:
            yield row


class Transformer:
    def transform_record(self, data):
        raise NotImplementedError

    def transform(self, data):
        if isinstance(data, dict):
            return self.transform_record(data)
        else:
            for row in data:
                yield self.transform_record(row)


class GutenbergTransformer(Transformer):
    def transform_record(self, data):
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
