import json
from pprint import pprint

from flask import current_app


def test_es_index(app, db, es):
    index_name = "test_index"
    try:
        path = current_app.extensions['invenio-search'].mappings["test"]
        with open(path) as fp:
            mapping = json.load(fp)
        assert "properties" in mapping["mappings"]["properties"]["test"].keys()
        if not es.indices.exists(index=index_name):
            es.indices.create(index_name, body=mapping)
        record = {
            "test": [
                {
                    "is_ancestor": True,
                    "links": {
                        "self": "https://localhost/api/2.0/taxonomies/level-1",
                    },
                    "level": 1
                },
                {
                    "is_ancestor": False,
                    "links": {
                        "self": "https://localhost/api/2.0/taxonomies/level-1/level-2",
                        "parent": "https://localhost/api/2.0/taxonomies/level-1"
                    },
                    "level": 2
                }
            ]
        }
        es.index(index=index_name, id=1, body=record)
    finally:
        if es.indices.exists(index=index_name):
            es.indices.delete(index_name)
