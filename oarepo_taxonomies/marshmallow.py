import copy
import re
from urllib.parse import urlparse

import deepmerge
from boltons.iterutils import remap
from marshmallow import Schema, INCLUDE, pre_load, ValidationError, post_load
from marshmallow.fields import Boolean, Nested
from oarepo_references.mixins import InlineReferenceMixin, ReferenceFieldMixin
from oarepo_taxonomies.utils import get_taxonomy_json
from sqlalchemy.orm.exc import NoResultFound


class TaxonomyTermMerger:
    def __init__(self):
        self.taxonomy_terms = {}
        self.validated_terms = set()

    def add_reference(self, ref):
        slug, taxonomy_code = get_slug_from_link(ref)
        try:
            term_array = get_taxonomy_json(code=taxonomy_code, slug=slug).paginated_data
            for term in term_array:
                link = self.term_link(term)
                self._add_term_internal(link, term)
                self.validated_terms.add(link)
        except NoResultFound:
            raise ValidationError(f"Taxonomy term '{taxonomy_code}/{slug}' has not been found")

    def _add_term_internal(self, link, term):
        if link in self.taxonomy_terms:
            deepmerge.always_merger.merge(self.taxonomy_terms[link], term)
        else:
            self.taxonomy_terms[link] = copy.deepcopy(term)

    def add_term(self, term):
        link = self.term_link(term)
        self._add_term_internal(link, term)
        if term.get('is_ancestor', False):
            # do not fetch ancestor
            return

        # fetch and merge the term and ancestors
        self.add_reference(link)

    def term_link(self, term):
        link = term.get('links', {}).get('self', None)
        if not link:
            raise ValidationError('self link not found on %s' % term)
        return link

    def get_merged_terms(self):
        ret = [x for link, x in self.taxonomy_terms.items() if link in self.validated_terms]
        ret.sort(key=lambda x: (not x['is_ancestor'], self.term_link(x)))
        ret = remap(ret, lambda p, k, v: v is not None)
        return ret


class TaxonomyNested(Nested):
    def _test_collection(self, value):
        # the taxonomy schema will make the value array even if it is not,
        # so do not check if collection or not
        pass


def TaxonomyField(*args, extra=None, name=None, many=False, mixins: list = None, **kwargs):
    mixins = mixins or []
    extra = extra or {}

    required = kwargs.pop('required', False)

    if extra or mixins:
        base_tuple = (TaxonomySchema, *mixins)
        t = type(name or ('TaxonomyFieldWithExtra_' +
                          ''.join(x.__name__ for x in mixins) +
                          '_' + '_'.join(extra.keys())),
                 base_tuple, extra or {})
    else:
        t = TaxonomySchema

    taxonomy_schema = t(*args, many=many, **kwargs)
    return TaxonomyNested(taxonomy_schema, required=required, many=True)


class TaxonomySchema(Schema, ReferenceFieldMixin):
    class Meta:
        unknown = INCLUDE

    def __init__(self, *args, **kwargs):
        self.internal_many = kwargs.pop('many', False)
        kwargs['many'] = True
        super(TaxonomySchema, self).__init__(*args, **kwargs)

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
        if in_data is None:
            return None

        if not isinstance(in_data, (list, tuple)):
            in_data = [in_data]

        changes = self.context.get('changed_reference', None)
        if changes:
            # called with changed_reference => check if the reference is ours and if not, just
            # return the previous data
            for d in in_data:
                if d['links']['self'] == changes['url']:
                    break
            else:
                return in_data

        changes = self.context.get('renamed_reference', None)
        if changes:
            new_data = []
            for x in in_data:
                if isinstance(x, dict) and x.get('links', {}).get('self') == changes['old_url']:
                    new_data.append(changes['new_url'])
                    continue
                new_data.append(x)
            in_data = new_data

        term_merger = TaxonomyTermMerger()
        for term in in_data:
            if isinstance(term, str):
                term_merger.add_reference(term)
            else:
                term_merger.add_term(term)

        in_data = term_merger.get_merged_terms()

        for term in in_data:
            if not term.get('is_ancestor'):
                self.register(term['links']['self'], inline=True)

        return in_data

    @post_load(pass_many=True)
    def check_many(self, data, *args, **kwargs):
        if not self.internal_many:
            terms = [x for x in data if not x['is_ancestor']]
            if len(terms) > 1:
                raise ValidationError('Expected one taxonomy term but %s found: %s' % (len(terms), terms))
        return data


def get_slug_from_link(link):
    url = urlparse(link)
    if "taxonomies" not in url.path:
        raise ValueError(f"Link '{link}' is not taxonomy reference")
    taxonomy_slug = url.path.split("taxonomies/")[-1].split("/")
    taxonomy_code = taxonomy_slug.pop(0)
    slug = "/".join(taxonomy_slug)
    return slug, taxonomy_code


# TODO: nepouzivat
def extract_link(text):
    # https://stackoverflow.com/questions/839994/extracting-a-url-in-python
    regex = re.search("(?P<url>https?://[^\s]+)", text)
    if not regex:
        return
    url = regex.group("url")
    return url
