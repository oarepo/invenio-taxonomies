from flask import Flask

from invenio_taxonomies.ext import InvenioTaxonomies


def test_version():
    """Test version import."""
    from invenio_taxonomies.version import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    InvenioTaxonomies(app)
    assert 'flask-taxonomies' in app.extensions

    app = Flask('testapp')
    ext = InvenioTaxonomies()
    assert 'flask-taxonomies' not in app.extensions
    ext.init_app(app)
    assert 'flask-taxonomies' in app.extensions
    assert app.blueprints['flask_taxonomies']
