import click
from flask import cli
from flask.cli import with_appcontext
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


@taxonomies.command('import')
@click.argument('taxonomy_file')
@click.option('--int', 'int_conversions', multiple=True)
@click.option('--str', 'str_args', multiple=True)
@click.option('--bool', 'bool_args', multiple=True)
@click.option('--drop/--no-drop', default=False)
@with_appcontext
def import_taxonomy(taxonomy_file, int_conversions, str_args, bool_args, drop):
    from .import_export import import_taxonomy
    import_taxonomy(taxonomy_file, int_conversions, str_args, bool_args, drop)


@taxonomies.command('export')
@click.argument('taxonomy_code')
@with_appcontext
def export_taxonomy(taxonomy_code):
    from .import_export import export_taxonomy
    export_taxonomy(taxonomy_code)
