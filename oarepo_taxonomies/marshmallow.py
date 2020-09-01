import re
from urllib.parse import urlparse

from marshmallow import Schema, INCLUDE, pre_load, ValidationError, post_load
from marshmallow.fields import Boolean
from oarepo_references.mixins import InlineReferenceMixin
from sqlalchemy.orm.exc import NoResultFound

from oarepo_taxonomies.utils import get_taxonomy_json


class TaxonomyField(Schema, InlineReferenceMixin):
    class Meta:
        unknown = INCLUDE

    is_ancestor = Boolean(required=False)

    def ref_url(self, data):
        if isinstance(data, (list, tuple)):
            data = data[-1]
        return data.get('links', {}).get('self', None)

    @pre_load(pass_many=True)
    def resolve_links(self, in_data, **kwargs):
        """
        Transform input data to dict, find link and resolve taxonomy. Taxonomy must always be
        list due to ElasticSearch reason, but transformation to list is processed in post_load
        function.
        """
        if isinstance(in_data, (list, tuple)):
            in_data = in_data[-1]
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
            if self.context:
                renamed_reference = self.context.get("renamed_reference")
                if renamed_reference:
                    link = renamed_reference["new_url"]
            slug, taxonomy_code = get_slug_from_link(link)
            try:
                taxonomy_array = get_taxonomy_json(code=taxonomy_code, slug=slug).paginated_data
                taxonomy_json = taxonomy_array.pop()
                in_data.update(taxonomy_json)
                if self.many:
                    taxonomy_array.append(in_data)
                    return taxonomy_array
                return in_data

            except NoResultFound:
                raise NoResultFound(f"Taxonomy '{taxonomy_code}/{slug}' has not been found")
            except:
                raise
        else:
            raise ValidationError("Input data does not contain link to taxonomy reference")

    @post_load(pass_many=True)
    def get_list(self, in_data, **kwargs):
        if isinstance(in_data, list):
            return in_data
        return create_list(in_data)


def create_list(in_data):
    link = in_data["links"]["self"]
    slug, taxonomy_code = get_slug_from_link(link)
    taxonomy_array = get_taxonomy_json(code=taxonomy_code, slug=slug).paginated_data
    taxonomy_array[-1] = in_data
    return taxonomy_array


def extract_link(text):
    # https://stackoverflow.com/questions/839994/extracting-a-url-in-python
    regex = re.search("(?P<url>https?://[^\s]+)", text)
    if not regex:
        return
    url = regex.group("url")
    return url


def get_slug_from_link(link):
    url = urlparse(link)
    if "taxonomies" not in url.path:
        raise ValueError(f"Link '{link}' is not taxonomy reference")
    taxonomy_slug = url.path.split("taxonomies/")[-1].split("/")
    taxonomy_code = taxonomy_slug.pop(0)
    slug = "/".join(taxonomy_slug)
    return slug, taxonomy_code
