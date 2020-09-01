from flask_taxonomies.models import TaxonomyTerm
from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.term_identification import TermIdentification


def test_create_taxonomy(app, db):
    """
    Test if creating taxonomy working. Test uses SQLite db.
    """

    # management task that creates flask-taxonomies tables
    # subprocess.run(["invenio", "taxonomies", "init"])

    current_flask_taxonomies.create_taxonomy("root", extra_data={}, session=db.session)
    db.session.commit()
    res = current_flask_taxonomies.list_taxonomies(session=db.session).all()
    print(res)
    assert len(res) == 1


def test_api(app, db):
    taxonomy = current_flask_taxonomies.create_taxonomy("root", extra_data={}, session=db.session)
    db.session.commit()

    identification = TermIdentification(taxonomy=taxonomy, slug="a")
    term = current_flask_taxonomies.create_term(identification, extra_data={"a": 1})
    assert term.slug == "a"
    db.session.commit()

    identification2 = TermIdentification(parent=term, slug="b")
    term2 = current_flask_taxonomies.create_term(identification2, extra_data={"b": 2})
    assert term2.slug == "a/b"
    db.session.commit()

    res = current_flask_taxonomies.list_taxonomies().all()
    print(res)

    # filter
    term_identification = TermIdentification(taxonomy=taxonomy, slug=term.slug)
    assert list(current_flask_taxonomies.filter_term(
        term_identification)) == [term]

    assert list(current_flask_taxonomies.filter_term(
        TermIdentification(taxonomy=taxonomy, slug=term2.slug))) == [term2]

    res_term = current_flask_taxonomies.filter_term(term_identification).one_or_none()
    assert isinstance(res_term, TaxonomyTerm)


def test_move_term(app, db, taxonomy_tree):
    taxonomy = current_flask_taxonomies.get_taxonomy("test_taxonomy")
    terms = current_flask_taxonomies.list_taxonomy(taxonomy).all()
    print(terms)
    ti = TermIdentification(term=terms[2])
    current_flask_taxonomies.move_term(ti, new_parent=terms[0], remove_after_delete=False)
    db.session.commit()
    terms = current_flask_taxonomies.list_taxonomy(taxonomy).all()
    print(terms)
