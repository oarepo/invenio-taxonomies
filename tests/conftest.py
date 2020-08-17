from __future__ import absolute_import, print_function

import os
import shutil
import tempfile
from pathlib import Path

import pytest
from flask import Flask
from invenio_db import InvenioDB
from invenio_db import db as db_
from sqlalchemy_utils import database_exists, create_database, drop_database

from invenio_taxonomies.ext import InvenioTaxonomies


@pytest.yield_fixture()
def app():
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        JSONSCHEMAS_HOST="nusl.cz",
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        # SQLALCHEMY_DATABASE_URI=os.environ.get(
        #     'SQLALCHEMY_DATABASE_URI',
        #     'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="oarepo", pw="oarepo",
        #                                                           url="127.0.0.1",
        #                                                           db="oarepo")),
        SERVER_NAME='127.0.0.1:5000',
    )

    InvenioDB(app)
    InvenioTaxonomies(app)
    with app.app_context():
        # app.register_blueprint(taxonomies_blueprint)
        yield app

    shutil.rmtree(instance_path)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    dir_path = os.path.dirname(__file__)
    parent_path = str(Path(dir_path).parent)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            f'sqlite:////{parent_path}/database.db')
    )
    drop_database(db_.engine.url)
    if not database_exists(str(db_.engine.url)):
        create_database(db_.engine.url)
    db_.create_all()

    yield db_

    # Explicitly close DB connection
    db_.session.close()
    db_.drop_all()
