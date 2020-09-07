import sqlalchemy
from flask_taxonomies.constants import INCLUDE_DELETED, INCLUDE_DESCENDANTS, \
    INCLUDE_DESCENDANTS_COUNT, INCLUDE_STATUS, INCLUDE_SELF
from flask_taxonomies.models import TaxonomyTerm, TermStatusEnum, Representation
from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.term_identification import TermIdentification
from flask_taxonomies.views.common import build_descendants
from flask_taxonomies.views.paginator import Paginator


def get_taxonomy_json(code=None,
                      slug=None,
                      prefer: Representation = Representation("taxonomy"),
                      page=None,
                      size=None,
                      status_code=200,
                      q=None,
                      request=None):
    taxonomy = current_flask_taxonomies.get_taxonomy(code)
    prefer = taxonomy.merge_select(prefer)

    if request:
        current_flask_taxonomies.permissions.taxonomy_term_read.enforce(request=request,
                                                                        taxonomy=taxonomy,
                                                                        slug=slug)

    if INCLUDE_DELETED in prefer:
        status_cond = sqlalchemy.sql.true()
    else:
        status_cond = TaxonomyTerm.status == TermStatusEnum.alive

    return_descendants = INCLUDE_DESCENDANTS in prefer

    if return_descendants:
        query = current_flask_taxonomies.descendants_or_self(
            TermIdentification(taxonomy=code, slug=slug),
            levels=prefer.options.get('levels', None),
            status_cond=status_cond,
            return_descendants_count=INCLUDE_DESCENDANTS_COUNT in prefer,
            return_descendants_busy_count=INCLUDE_STATUS in prefer
        )
    else:
        query = current_flask_taxonomies.filter_term(
            TermIdentification(taxonomy=code, slug=slug),
            status_cond=status_cond,
            return_descendants_count=INCLUDE_DESCENDANTS_COUNT in prefer,
            return_descendants_busy_count=INCLUDE_STATUS in prefer
        )
    if q:
        query = current_flask_taxonomies.apply_term_query(query, q, code)
    paginator = Paginator(
        prefer,
        query, page if return_descendants else None,
        size if return_descendants else None,
        json_converter=lambda data:
        build_descendants(data, prefer, root_slug=None),
        allow_empty=INCLUDE_SELF not in prefer, single_result=INCLUDE_SELF in prefer,
        has_query=q is not None
    )
    return paginator


# def unlock_term(term_url):
#     slug, taxonomy_code = get_slug_from_link(term_url)
#     term_identification = TermIdentification(taxonomy=taxonomy_code, slug=slug)
#     term = list(current_flask_taxonomies.filter_term(
#         term_identification))[0]
#     busy_count_0 = term.busy_count
#     current_flask_taxonomies.unmark_busy([term.id])
#     assert term.busy_count < busy_count_0
