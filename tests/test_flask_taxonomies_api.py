import subprocess

from flask_taxonomies.proxies import current_flask_taxonomies


def test_create_taxonomy(app, db):
    """
    Test if creating taxonomy working
    """

    # management task that creates flask-taxonomies tables
    subprocess.run(["invenio", "taxonomies", "init"])

    current_flask_taxonomies.create_taxonomy("root", extra_data={}, session=db.session)
    db.session.commit()
    res = current_flask_taxonomies.list_taxonomies(session=db.session).all()
    print(res)
    assert len(res) == 1
