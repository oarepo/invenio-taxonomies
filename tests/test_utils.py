from pprint import pprint

from flask_taxonomies.constants import *
from flask_taxonomies.models import Representation

from oarepo_taxonomies.utils import get_taxonomy_json


def test_get_taxonomy_json(app, db, taxonomy_tree):
    paginator = get_taxonomy_json(code="test_taxonomy", slug="a/b")
    res = paginator.paginated_data
    assert isinstance(res, list)
    for item in res:
        assert "ancestors" not in item.keys()
        assert "children" not in item.keys()
        assert "links" in item.keys()


def test_get_taxonomy_json_2(app, db, taxonomy_tree):
    paginator = get_taxonomy_json(code="test_taxonomy", slug="a/b",
                                  prefer=Representation("representation",
                                                        include=[INCLUDE_DESCENDANTS]))
    res = paginator.paginated_data
    assert "children" in res.keys()


def test_get_taxonomy_json_3(app, db, taxonomy_tree):
    include = [INCLUDE_URL, INCLUDE_DESCENDANTS_URL, INCLUDE_DESCENDANTS_COUNT,
               INCLUDE_ANCESTORS_HIERARCHY, INCLUDE_ANCESTORS, INCLUDE_ANCESTOR_LIST, INCLUDE_DATA,
               INCLUDE_ID, INCLUDE_DESCENDANTS, INCLUDE_ENVELOPE, INCLUDE_DELETED, INCLUDE_SLUG,
               INCLUDE_LEVEL, INCLUDE_STATUS, INCLUDE_SELF]
    paginator = get_taxonomy_json(code="test_taxonomy", slug="a/b",
                                  prefer=Representation("representation",
                                                        include=include))
    res = paginator.paginated_data
    pprint(res)


def test_get_taxonomy_json_4(app, db, taxonomy_tree):
    paginator = get_taxonomy_json(code="test_taxonomy", slug="a/b")
    res = paginator.paginated_data
    pprint(res)
