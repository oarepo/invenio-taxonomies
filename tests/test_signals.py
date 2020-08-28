from flask_taxonomies.signals import before_taxonomy_deleted


def test_taxonomy_delete(app):
    before_taxonomy_deleted.send("ahoj")