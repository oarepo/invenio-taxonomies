def test_init_db(app, db):
    assert db.engine.has_table("taxonomy_taxonomy")
    assert db.engine.has_table("taxonomy_term")
