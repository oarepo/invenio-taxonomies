from flask import current_app


def test_init(app, schema):
    schemas = current_app.extensions["invenio-jsonschemas"].schemas
    assert "taxonomy-v2.0.0.json" in schemas.keys()

# TODO: spravit test
# def test_validate(app, record, schema):
#     print(current_jsonschemas.schemas)
#     _records_state.validate(record,
#                             "https://example.com/schemas/test_schema-v1.0.0.json")
