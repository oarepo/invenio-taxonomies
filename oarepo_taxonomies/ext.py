from flask_taxonomies.ext import FlaskTaxonomies
from flask_taxonomies.signals import before_taxonomy_deleted, before_taxonomy_term_deleted, \
    before_taxonomy_term_moved, after_taxonomy_term_moved, after_taxonomy_term_updated, \
    before_taxonomy_term_updated
from flask_taxonomies.views import blueprint

from oarepo_taxonomies.signals import taxonomy_delete, taxonomy_term_moved, taxonomy_term_delete, \
    taxonomy_term_update, lock_term


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

        # connect signals
        before_taxonomy_deleted.connect(taxonomy_delete)
        before_taxonomy_term_deleted.connect(taxonomy_term_delete)
        before_taxonomy_term_updated.connect(lock_term)
        after_taxonomy_term_updated.connect(taxonomy_term_update)
        before_taxonomy_term_moved.connect(lock_term)
        after_taxonomy_term_moved.connect(taxonomy_term_moved)

    def init_config(self, app):
        from oarepo_taxonomies import config
        app.config["FLASK_TAXONOMIES_REPRESENTATION"] = {
            **config.FLASK_TAXONOMIES_REPRESENTATION,
            **app.config[
                "FLASK_TAXONOMIES_REPRESENTATION"]
        }
