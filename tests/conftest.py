from __future__ import absolute_import, print_function

import json
import os
import pathlib
import shutil
import subprocess
import tempfile
from collections import namedtuple
from pathlib import Path

import pytest
from flask import Flask, make_response
from flask_login import LoginManager, login_user
from flask_principal import RoleNeed, Principal, Permission
from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.term_identification import TermIdentification
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_accounts.models import User, Role
from invenio_base.signals import app_loaded
from invenio_db import InvenioDB
from invenio_db import db as db_
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_records_rest.views import create_blueprint_from_app
from invenio_search import InvenioSearch
from oarepo_mapping_includes.ext import OARepoMappingIncludesExt
from sqlalchemy_utils import database_exists, create_database, drop_database

from oarepo_taxonomies.ext import OarepoTaxonomies
from tests.helpers import set_identity


@pytest.yield_fixture()
def app(mapping):
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SERVER_NAME='127.0.0.1:5000',
        INVENIO_INSTANCE_PATH=instance_path,
        DEBUG=True,
        FLASK_TAXONOMIES_URL_PREFIX='/2.0/taxonomies/'
        # in tests, api is not on /api but directly in the root
    )
    app.secret_key = 'changeme'
    print(os.environ.get("INVENIO_INSTANCE_PATH"))

    InvenioDB(app)
    OarepoTaxonomies(app)
    InvenioAccounts(app)
    InvenioAccess(app)
    Principal(app)
    InvenioJSONSchemas(app)
    InvenioSearch(app)
    OARepoMappingIncludesExt(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def basic_user_loader(user_id):
        user_obj = User.query.get(int(user_id))
        return user_obj

    app.register_blueprint(create_blueprint_from_app(app))

    @app.route('/test/login/<int:id>', methods=['GET', 'POST'])
    def test_login(id):
        print("test: logging user with id", id)
        response = make_response()
        user = User.query.get(id)
        login_user(user)
        set_identity(user)
        return response

    app.extensions['invenio-search'].mappings["test"] = mapping

    app_loaded.send(app, app=app)

    with app.app_context():
        # app.register_blueprint(taxonomies_blueprint)
        yield app

    shutil.rmtree(instance_path)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    dir_path = os.path.dirname(__file__)
    parent_path = str(Path(dir_path).parent)
    db_path = os.environ.get('SQLALCHEMY_DATABASE_URI', f'sqlite:////{parent_path}/database.db')
    os.environ["INVENIO_SQLALCHEMY_DATABASE_URI"] = db_path
    app.config.update(
        SQLALCHEMY_DATABASE_URI=db_path
    )
    if database_exists(str(db_.engine.url)):
        drop_database(db_.engine.url)
    if not database_exists(str(db_.engine.url)):
        create_database(db_.engine.url)
    db_.create_all()
    subprocess.run(["invenio", "taxonomies", "init"])
    yield db_

    # Explicitly close DB connection
    db_.session.close()
    db_.drop_all()


@pytest.fixture
def client(app, db):
    from flask_taxonomies.models import Base
    Base.metadata.create_all(db.engine)
    return app.test_client()


@pytest.fixture
def permission_client(app, db):
    app.config.update(
        FLASK_TAXONOMIES_PERMISSION_FACTORIES={
            'taxonomy_create': [Permission(RoleNeed('admin'))],
            'taxonomy_update': [Permission(RoleNeed('admin'))],
            'taxonomy_delete': [Permission(RoleNeed('admin'))],

            'taxonomy_term_create': [Permission(RoleNeed('admin'))],
            'taxonomy_term_update': [Permission(RoleNeed('admin'))],
            'taxonomy_term_delete': [Permission(RoleNeed('admin'))],
            'taxonomy_term_move': [Permission(RoleNeed('admin'))],
        }
    )
    from flask_taxonomies.models import Base
    Base.metadata.create_all(db.engine)
    return app.test_client()


@pytest.fixture
def tax_url(app):
    url = app.config['FLASK_TAXONOMIES_URL_PREFIX']
    if not url.endswith('/'):
        url += '/'
    return url


@pytest.fixture
def taxonomy(app, db):
    taxonomy = current_flask_taxonomies.create_taxonomy("test_taxonomy", extra_data={
        "title":
            {
                "cs": "test_taxonomy",
                "en": "test_taxonomy"
            }
    })
    db.session.commit()
    return taxonomy


@pytest.fixture
def taxonomy_tree(app, db, taxonomy):
    id1 = TermIdentification(taxonomy=taxonomy, slug="a")
    term1 = current_flask_taxonomies.create_term(id1, extra_data={"test": "extra_data"})
    id2 = TermIdentification(parent=term1, slug="b")
    term2 = current_flask_taxonomies.create_term(id2, extra_data={"test": "extra_data"})
    id3 = TermIdentification(taxonomy=taxonomy, slug="a/b/c")
    term3 = current_flask_taxonomies.create_term(id3, extra_data={"test": "extra_data"})
    db.session.commit()


TestUsers = namedtuple('TestUsers', ['u1', 'u2', 'u3', 'r1', 'r2'])


@pytest.fixture()
def test_users(app, db):
    """Returns named tuple (u1, u2, u3, r1, r2)."""
    with db.session.begin_nested():
        r1 = Role(name='admin')
        r2 = Role(name='role2')

        u1 = User(id=1, email='1@test.com', active=True, roles=[r1])
        u2 = User(id=2, email='2@test.com', active=True, roles=[r1, r2])
        u3 = User(id=3, email='3@test.com', active=True, roles=[r2])

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)

        db.session.add(r1)
        db.session.add(r2)
    db.session.commit()

    return TestUsers(u1, u2, u3, r1, r2)


@pytest.fixture()
def mapping():
    parent_dir = pathlib.Path(__file__).parent.absolute()
    return str(parent_dir / "test_v1.0.0.json")
