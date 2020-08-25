import json
from pprint import pprint

from flask import current_app


def test_init(app):
    path = current_app.extensions['invenio-search'].mappings["test"]
    with open(path) as fp:
        mapping = json.load(fp)
    assert "properties" in mapping["mappings"]["properties"]["language"].keys()
    pprint(mapping)