import json
from collections import namedtuple, defaultdict
from typing import Iterable

from flask_taxonomies.api import TaxonomyTerm
from flask_taxonomies.api import TermStatusEnum
from invenio_db import db
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import joinedload


def bulk_taxonomy_query(
        taxonomy_code,
        query_data,
        query_function,
        result_preprocess_function,
        result_match_function
):
    """
    Selects taxonomy terms by multiple search criteria.

    It works the following way:

      1. query_data is an array of query criteria (for example, titles).
         Each criterium (c) is converted to DB query via query_function(c).
      2. Terms are filtered

    :param taxonomy_code:       the taxonomy code
    :param query_data:          array of query criteria
    :param query_function:      function converting query criterium to DB query
    :param result_preprocess_function:      function for preprocessing terms from DB
    :param result_match_function:   function that matches pre-processed terms query criteria
    :return:
    """
    all_terms = db.session.query(TaxonomyTerm.id, TaxonomyTerm.parent_id).filter(
        TaxonomyTerm.taxonomy_code == taxonomy_code,
        TaxonomyTerm.status == TermStatusEnum.alive
    )
    terms = all_terms
    q = []
    for d in query_data:
        q.append(query_function(d))
    terms = terms.filter(or_(*q))
    terms = terms.cte('cte', recursive=True)

    ancestors = all_terms.join(terms, TaxonomyTerm.id == terms.c.parent_id)

    recursive_q = terms.union(ancestors)
    q = db.session.query(recursive_q)
    ids = [x[0] for x in q]
    terms = {
        t.id: t for t in
        db.session
            .query(TaxonomyTerm)
            .options(joinedload(TaxonomyTerm.taxonomy, innerjoin=True))
            .filter(TaxonomyTerm.id.in_(ids))
    }
    parent_terms = set(t.parent_id for t in terms.values())
    leaf_terms = {
        k: v for k, v in terms.items() if k not in parent_terms
    }
    ctx = result_preprocess_function(leaf_terms, terms)
    for d in query_data:
        match = result_match_function(d, ctx)
        if match:
            yield d, match[0][0][-1]
        else:
            yield d, 0


ExtraField = namedtuple('ExtraField', 'field_array, priority, single_value')


def title_taxonomy_query(
        taxonomy_code,
        fields: Iterable[ExtraField],
        title_function,
        data
):
    def query_function(d):
        titles = title_function(d)
        or_query = []
        for fld in fields:
            if fld.single_value:
                or_query.append(
                    func.jsonb_extract_path_text(
                        TaxonomyTerm.extra_data, *fld.field_array
                    ) == titles[-1]
                )
            else:
                or_query.append(
                    func.jsonb_extract_path(
                        TaxonomyTerm.extra_data, *fld.field_array).op('?')(
                        titles[-1])
                )
        return and_(
            TaxonomyTerm.level == len(titles) - 1,
            or_(*or_query)
        )

    def deep_get(d, flds):
        for fld in flds:
            d = d.get(fld)
            if not d:
                break
        return d

    def result_preprocess_function(leaf_terms, terms):
        candidates = namedtuple('candidates', 'titles, leaf_terms') \
            (defaultdict(list), leaf_terms)
        for t in terms.values():
            for fld in fields:
                n = deep_get(t.extra_data, fld.field_array)
                if n:
                    for nn in [n] if fld.single_value else n:
                        candidates.titles[(nn, t.level)].append((t, fld.priority))
        return candidates

    def result_match_function(d, ctx):
        possibilities = None
        titles = title_function(d)
        for level, title in reversed(list(enumerate(titles))):
            found = ctx.titles.get((title, level), [])
            if possibilities is None:
                possibilities = [
                    ([x[0]], x[1]) for x in found
                ]
            else:
                found = {
                    x[0].id: x for x in found
                }
                filtered_possibilities = []
                for p in possibilities:
                    if p[0][0].parent_id in found:
                        f = found[p[0][0].parent_id]
                        filtered_possibilities.append((
                            [
                                f[0],
                                *p[0]
                            ],
                            f[1] + p[1]
                        ))
                possibilities = filtered_possibilities
        possibilities.sort(key=lambda x: x[1])
        return possibilities

    return bulk_taxonomy_query(
        taxonomy_code,
        data,
        query_function,
        result_preprocess_function,
        result_match_function
    )
