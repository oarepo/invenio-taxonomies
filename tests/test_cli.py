import subprocess


def test_init_db(app, db):
    # subprocess.run(["invenio", "taxonomies", "init"])
    assert db.engine.has_table("taxonomy_taxonomy")
    assert db.engine.has_table("taxonomy_term")
