from flask_taxonomies.constants import INCLUDE_DESCENDANTS
from flask_taxonomies.models import Representation

from oarepo_taxonomies.utils import get_taxonomy_json


def test_get_taxonomy_term(app, db, taxonomy_tree):
    paginator = get_taxonomy_json(code="test_taxonomy", slug="a/b")
    res = paginator.paginated_data
    assert isinstance(res, dict)
    assert "ancestors" in res.keys()
    assert "children" not in res.keys()
    assert "links" in res.keys()


def test_get_taxonomy_term_2(app, db, taxonomy_tree):
    paginator = get_taxonomy_json(code="test_taxonomy", slug="a/b",
                                  prefer=Representation("representation",
                                                        include=[INCLUDE_DESCENDANTS]))
    res = paginator.paginated_data
    assert "children" in res.keys()
