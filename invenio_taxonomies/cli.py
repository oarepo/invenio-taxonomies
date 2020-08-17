import click
from flask import cli
from flask_taxonomies.models import Base
from invenio_db import db as db_
from sqlalchemy_utils import database_exists, create_database


@click.group()
def taxonomies():
    """Taxonomies commands."""


@taxonomies.command("init")
@cli.with_appcontext
def init_db():
    """
    Management task that initialize database tables.
    """
    engine = db_.engine
    if not database_exists(engine.url):  # pragma: no cover
        create_database(engine.url)
    Base.metadata.create_all(engine)
