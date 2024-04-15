import re
import elasticsearch
from elasticsearch import Elasticsearch
from datasets import load_dataset






index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": ["lowercase", "asciifolding"]
                },
                "no_punc": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": [
                        "html_strip", "punctuation"
                    ],
                    "filter": [
                        "lowercase", "asciifolding", "unique",
                    ]
                },
                "standard_english": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": [
                        "english_poss_stemmer",
                        "lowercase", "asciifolding",
                        "english_stop", "english_stemmer",
                    ],
                },
                "bigram": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": ["lowercase", "asciifolding", "bigram"]
                },
                "trigram": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": ["lowercase", "asciifolding", "trigram"]
                }
            },
            "char_filter": {
                "punctuation": {
                    "type": "mapping",
                    "mappings": [".=>", ". =>"]
                }
            },
            "filter": {
                "en_stop": {
                    "type": "stop",
                    "stopwords": "_english_",
                },
                "en_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "en_poss_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "bigram": {
                    "type": "shingle",
                    "min_shingle_size": 2,
                    "max_shingle_size": 2,
                    "output_unigrams": False
                },
                "trigram": {
                    "type": "shingle",
                    "min_shingle_size": 3,
                    "max_shingle_size": 3,
                    "output_unigrams": False
                },
                "min_2_chars": {
                    "type": "length",
                    "min": 2,
                },
                "trunc_20_chars": {
                    "type": "truncate",
                    "length": 20,
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "text": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "standard_english"
                    }
                }
            },
            "title": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "standard_english"
                    }
                }
            },
            "author": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "english": {
                        "type": "text",
                        "analyzer": "standard_english"
                    }
                }
            }
        }
    }
}
index_name = 'gutenberg'


# Ingester
#   - Read a dataset
#   - Perform transformations
#   - Index the data





def search(es, index_name, qs):
    query = {
        "query": {
            "bool": {
                # TODO: Put a constant score here to make sure 75% of the terms are present
                # "filter": [],
                "should": [
                    # Match all the terms in order
                    {
                        "multi_match": {
                            "query": qs,
                            "type": "phrase",
                            "slop": 1,
                            "fields": ["text", "author", "title"],
                            "boost": 10,
                        },
                    },
                    # Match all the terms in one field
                    {
                        "multi_match": {
                            "query": qs,
                            "type": "best_fields",
                            "operator": "and",
                            "fields": ["text", "author", "title"],
                            "fuzziness": "AUTO",
                            "prefix_length": 1,
                            "boost": 5,
                        },
                    },
                    # Match all the terms across subfields, picking the best one
                    {
                        "dis_max": {
                            "queries": [
                                {
                                    "multi_match": {
                                        "query": qs,
                                        "fields": ["text", "text.english"],
                                        "type": "most_fields",
                                        "fuzziness": "AUTO",
                                        "prefix_length": 1,
                                        "operator": "and"
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": qs,
                                        "fields": ["title", "title.english"],
                                        "type": "most_fields",
                                        "fuzziness": "AUTO",
                                        "prefix_length": 1,
                                        "operator": "and"
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": qs,
                                        "fields": ["author", "author.english"],
                                        "type": "most_fields",
                                        "fuzziness": "AUTO",
                                        "prefix_length": 1,
                                        "operator": "and"
                                    }
                                }
                            ]
                        }
                    },
                    # Match all the terms across all fields
                    {
                        "dis_max": {
                            "queries": [
                                {
                                    "combined_fields": {
                                        "query": qs,
                                        "fields": ["text", "title", "author"],
                                        "operator": "and",
                                    },
                                    "combined_fields": {
                                        "query": qs,
                                        "fields": ["text.english", "title.english", "author.english"],
                                        "operator": "and",
                                    },
                                }
                            ],
                            "boost": 3,
                        }
                    },
                    # Match most terms across all fields
                    {
                        "dis_max": {
                            "queries": [
                                {
                                    "combined_fields": {
                                        "query": qs,
                                        "fields": ["text", "title", "author"],
                                        "operator": "or",
                                        "minimum_should_match": "2<-25%"
                                    },
                                    "combined_fields": {
                                        "query": qs,
                                        "fields": ["text.english", "title.english", "author.english"],
                                        "operator": "or",
                                        "minimum_should_match": "2<-25%"
                                    },
                                }
                            ],
                        }
                    },
                ]
            }
        }
    }
    result = es.search(
        index=index_name,
        body=query
    )
    hits = result['hits']['hits']
    return hits

search_gutenberg = lambda qs: search(es, 'gutenberg', qs)


result = es.search(
    index='gutenberg',
    body={"query": {"match_all": {}}}
)
result


[
    {'author': d['_source']['author'], 'title': d['_source']['title']}
    for d in  search(es, 'gutenberg', 'H. G. Wells')
]


def random_doc(es, index_name):
    result = es.search(
        index=index_name,
        body={"query": {"function_score": {"random_score": {}}}, "size": 1}
    )
    return result['hits']['hits'][0]['_source']


