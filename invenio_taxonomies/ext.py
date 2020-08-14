import os
from pathlib import Path

from flask_principal import Principal
from flask_taxonomies.ext import FlaskTaxonomies
from flask_taxonomies.views import blueprint
from sqlalchemy_utils import database_exists, create_database


class InvenioTaxonomies(object):
    """App Extension for Flask Taxonomies."""

    def __init__(self, app=None, db=None):
        """Extension initialization."""
        if app:
            self.init_app(app, db)

    def init_app(self, app, db=None):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['invenio-taxonomies'] = FlaskTaxonomies(app)
        Principal(app)
        app.register_blueprint(blueprint, url_prefix=app.config['FLASK_TAXONOMIES_URL_PREFIX'])
        self.init_db(app)

    def init_config(self, app):
        from invenio_taxonomies import config
        for k in dir(config):
            if k.startswith('FLASK_TAXONOMIES_'):
                app.config.setdefault(k, getattr(config, k))

    def init_db(self, app):
        from sqlalchemy import create_engine
        from flask_taxonomies.models import Base
        dir_path = os.path.dirname(__file__)
        parent_path = str(Path(dir_path).parent)
        app.config.update(
            SQLALCHEMY_DATABASE_URI=os.environ.get(
                'SQLALCHEMY_DATABASE_URI',
                f'sqlite:////{parent_path}/database.db')
        )
        db_path = app.config.get("SQLALCHEMY_DATABASE_URI")
        engine = create_engine(db_path)
        if not database_exists(engine.url):
            create_database(engine.url)
        Base.metadata.create_all(engine)
