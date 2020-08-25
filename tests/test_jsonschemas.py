from flask import current_app


def test_init(app):
    schemas = current_app.extensions["invenio-jsonschemas"].schemas
    assert "taxonomy-v2.0.0.json" in schemas.keys()
