from flask import Flask

from oarepo_taxonomies.ext import OarepoTaxonomies


def test_version():
    """Test version import."""
    from oarepo_taxonomies.version import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    OarepoTaxonomies(app)
    assert 'flask-taxonomies' in app.extensions

    app = Flask('testapp')
    ext = OarepoTaxonomies()
    assert 'flask-taxonomies' not in app.extensions
    ext.init_app(app)
    assert 'flask-taxonomies' in app.extensions
    assert app.blueprints['flask_taxonomies']
