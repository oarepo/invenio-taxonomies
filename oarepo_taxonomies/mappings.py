import deepmerge
from oarepo_mapping_includes import Mapping


def taxonomy_term(content=None, **kwargs):
    ret = {
        "type": "object",
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
            }
        }
    }
    ret = deepmerge.always_merger.merge(ret, content)
    ret['type'] = 'object'
    return Mapping(ret, merge=False)