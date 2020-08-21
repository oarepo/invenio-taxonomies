import re
from urllib.parse import urlparse

from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.term_identification import TermIdentification
from invenio_records_rest.schemas.fields import SanitizedUnicode
from marshmallow import Schema, INCLUDE, pre_load, ValidationError
from marshmallow.fields import Nested
from sqlalchemy.orm.exc import NoResultFound

from oarepo_taxonomies.utils import get_taxonomy_json


class TaxonomyLinksSchemaV1(Schema):
    self = SanitizedUnicode(required=False)
    tree = SanitizedUnicode(required=False)


class TaxonomyField(Schema):
    class Meta:
        unknown = INCLUDE

    links = Nested(TaxonomyLinksSchemaV1, required=False)

    @pre_load
    def resolve_links(self, in_data, **kwargs):
        if isinstance(in_data, dict):
            try:
                link = in_data["links"]["self"]
            except KeyError:
                link = None
        elif isinstance(in_data, str):
            link = extract_link(in_data)
            if link:
                in_data = {
                    "links": {
                        "self": link
                    }
                }
        else:
            raise TypeError("Input data have to be json or string")
        if link:
            slug, taxonomy_code = get_slug_from_link(link)
            try:
                in_data.update(**get_taxonomy_json(code=taxonomy_code, slug=slug).paginated_data)
            except NoResultFound:
                raise NoResultFound(f"Taxonomy '{taxonomy_code}/{slug}' has not been found")
        else:
            raise ValidationError("Input data does not contain link to taxonomy reference")
        return in_data


def extract_link(text):
    # https://stackoverflow.com/questions/839994/extracting-a-url-in-python
    regex = re.search("(?P<url>https?://[^\s]+)", text)
    if not regex:
        return
    url = regex.group("url")
    return url


def get_term_by_link(link):
    slug, taxonomy_code = get_slug_from_link(link)
    term = current_flask_taxonomies.filter_term(
        TermIdentification(taxonomy=taxonomy_code, slug=slug)).one_or_none()
    if not term:
        return None
    return term


def get_slug_from_link(link):
    url = urlparse(link)
    if "taxonomies" not in url.path:
        raise ValueError(f"Link '{link}' is not taxonomy reference")
    taxonomy_slug = url.path.split("taxonomies/")[-1].split("/")
    taxonomy_code = taxonomy_slug.pop(0)
    slug = "/".join(taxonomy_slug)
    return slug, taxonomy_code
