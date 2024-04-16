
import re

from datasets import load_dataset


def split_text_into_passages(
        text,
        split_characters=None,
        max_length=2000,
        min_length=100,
    ):
    if split_characters is None:
        split_characters = ['\n\n', '\n'] + list('.?!,')
    passages = []

    def split_recursively(text, split_chars):
        if len(text) <= max_length:
            passages.append(text)
            return

        if not len(split_chars):
            return

        split_char = split_chars[0]
        parts = text.split(split_char)

        for part in parts:
            if len(part) <= max_length:
                if (len(part) > 0):
                    passages.append(part)
            else:
                split_recursively(part, split_chars[1:])

    split_recursively(text, split_characters)
    return passages


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
            for idx, doc in enumerate(data):
                if idx % 100 == 0:
                    print(f'Indexed {idx} documents')
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
        result['passages'] = [
            {'text': passage} for passage
            in split_text_into_passages(result['text'])
        ]
        return result
