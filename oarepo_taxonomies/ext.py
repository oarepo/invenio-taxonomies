from flask_taxonomies.ext import FlaskTaxonomies
from flask_taxonomies.views import blueprint


class OarepoTaxonomies(object):
    """App Extension for Flask Taxonomies."""

    def __init__(self, app=None, db=None):
        """Extension initialization."""
        if app:
            self.init_app(app, db)

    def init_app(self, app, db=None):
        """Flask application initialization."""
        self.init_config(app)
        FlaskTaxonomies(app)
        app.register_blueprint(blueprint, url_prefix=app.config['FLASK_TAXONOMIES_URL_PREFIX'])

    def init_config(self, app):
        from oarepo_taxonomies import config
        for k in dir(config):
            if k.startswith('FLASK_TAXONOMIES_'):  # pragma: no cover
                app.config.setdefault(k, getattr(config, k))
