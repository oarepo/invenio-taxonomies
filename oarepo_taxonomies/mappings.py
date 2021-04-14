import deepmerge
from oarepo_mapping_includes import Mapping


def taxonomy_term(content=None, **kwargs):
    ret = {
        "type": "nested",
        "properties": {
            "is_ancestor": {
                "type": "boolean"
            },
            "links": {
                "type": "object",
                "properties": {
                    "self": {
                        "type": "keyword"
                    },
                    "parent": {
                        "type": "keyword"
                    }
                }
            },
            "level": {
                "type": "integer"
            }
        }
    }
    ret = deepmerge.always_merger.merge(ret, content)
    ret["type"] = "nested"
    return Mapping(ret, merge=False)