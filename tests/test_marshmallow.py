from pprint import pprint

import pytest
from flask_taxonomies.models import TaxonomyTerm
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from oarepo_taxonomies.marshmallow import TaxonomyField, extract_link, get_term_by_link, \
    get_slug_from_link


def test_resolve_links_random():
    """
    Test if random user data are passed.
    """
    random_user_data = {
        "created_at": "2014-08-11T05:26:03.869245",
        "email": "ken@yahoo.com",
        "name": "Ken",
        "test": "bla"
    }
    schema = TaxonomyField()
    with pytest.raises(ValidationError):
        schema.load(random_user_data)


def test_resolve_links_random_link(taxonomy_tree):
    """
    Test if random user data with link resolve taxonomy and keep user data.
    """
    random_user_data = {
        "created_at": "2014-08-11T05:26:03.869245",
        "email": "ken@yahoo.com",
        "name": "Ken",
        "links": {
            "self": "http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a/b"
        }
    }
    schema = TaxonomyField()
    res = schema.load(random_user_data)
    assert res == {
        'ancestors': [{
            'links': {
                'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a'
            },
            'test': 'extra_data'
        }],
        'created_at': '2014-08-11T05:26:03.869245',
        'email': 'ken@yahoo.com',
        'links': {'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a/b'},
        'name': 'Ken',
        'test': 'extra_data'
    }


def test_resolve_links_random_string(app, db, taxonomy_tree):
    """
    Test if random user data (string) are passed.
    """
    random_user_data = "bla bla http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a/b"
    schema = TaxonomyField()
    result = schema.load(random_user_data)
    assert result == {
        'ancestors': [{
            'links': {
                'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a'
            },
            'test': 'extra_data'
        }],
        'links': {'self': 'http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a/b'},
        'test': 'extra_data'
    }


def test_resolve_links_random_string_2(app, db, taxonomy_tree):
    """
    Test if random user data (string) are passed.
    """
    random_user_data = "bla bla http://example.com/"
    schema = TaxonomyField()
    with pytest.raises(ValueError):
        schema.load(random_user_data)


def test_resolve_links_random_string_3(app, db, taxonomy_tree):
    """
    Test if random user data (string) are passed.
    """
    random_user_data = "bla bla http://example.com/taxonomies/a/b/z"
    schema = TaxonomyField()
    with pytest.raises(NoResultFound):
        schema.load(random_user_data)


def test_resolve_links_random_string_4(app, db, taxonomy_tree):
    """
    Test if random user data (string) are passed.
    """
    random_user_data = "bla bla http://example.com/a/b/z"
    schema = TaxonomyField()
    with pytest.raises(ValueError):
        schema.load(random_user_data)


def test_resolve_links_random_string_5(app, db, taxonomy_tree):
    """
    Test if random user data (string) are passed.
    """
    random_user_data = ["wrong type"]
    schema = TaxonomyField()
    with pytest.raises(TypeError):
        schema.load(random_user_data)


def test_extract_link_1():
    url = extract_link("bla bla http://example.com/")
    assert url == "http://example.com/"


def test_extract_link_2():
    url = extract_link("bla bla")
    assert url is None


def test_get_term_by_link(taxonomy_tree):
    term = get_term_by_link("http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a/b")
    assert isinstance(term, TaxonomyTerm)


def test_get_term_by_link_2(taxonomy_tree):
    term = get_term_by_link("http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a/b/ble")
    assert term is None


def test_get_slug_from_link():
    slug, code = get_slug_from_link("http://127.0.0.1:5000/api/2.0/taxonomies/test_taxonomy/a/b")
    assert slug == "a/b"
    assert code == "test_taxonomy"
