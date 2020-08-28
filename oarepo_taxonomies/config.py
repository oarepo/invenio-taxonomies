from flask_taxonomies.constants import INCLUDE_DATA, INCLUDE_ANCESTORS, INCLUDE_URL, INCLUDE_SELF, \
    INCLUDE_ANCESTOR_LIST, INCLUDE_ANCESTOR_TAG, INCLUDE_PARENT

FLASK_TAXONOMIES_REPRESENTATION = {
    "taxonomy": {
        'include': [INCLUDE_DATA, INCLUDE_ANCESTORS, INCLUDE_URL, INCLUDE_SELF,
                    INCLUDE_ANCESTOR_LIST, INCLUDE_ANCESTOR_TAG, INCLUDE_PARENT],
        'exclude': [],
        'select': None,
        'options': {}
    }
}
