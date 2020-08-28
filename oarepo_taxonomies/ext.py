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
        FlaskTaxonomies(app)
        self.init_config(app)
        prefix = app.config['FLASK_TAXONOMIES_URL_PREFIX']
        if prefix.startswith('/api'):
            prefix = prefix[4:]
        app.register_blueprint(blueprint, url_prefix=prefix)

    def init_config(self, app):
        from oarepo_taxonomies import config
        app.config["FLASK_TAXONOMIES_REPRESENTATION"] = {
            **config.FLASK_TAXONOMIES_REPRESENTATION,
            **app.config[
                "FLASK_TAXONOMIES_REPRESENTATION"]
        }
