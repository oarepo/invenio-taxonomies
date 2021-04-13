from collections import defaultdict

from flask_babelex import get_locale
from flask_taxonomies.models import TaxonomyTerm, Taxonomy
from invenio_db import db


def bucket_level(bucket):
    return bucket["key"].split("/taxonomies/")[-1].rstrip("/").count("/")


def taxonomy_enabled_search(serializer, taxonomy_aggs, fallback_language="en"):
    def search(*args, search_result=None, **kwargs):
        if search_result is None:
            return serializer(*args, search_result=search_result, **kwargs)
        aggs = search_result.get("aggregations", [])
        aggs_by_key = defaultdict(list)
        for k in aggs.keys():
            aggs_by_key[k.rsplit(".", maxsplit=1)[0]].append(k)
        for taxonomy_agg in taxonomy_aggs:
            key = "nested#" + taxonomy_agg
            if key not in aggs_by_key:
                continue
            for aggs_key in aggs_by_key[key]:
                buckets = aggs[aggs_key]["sterms#links"]["buckets"]
                level = int(aggs_key.rsplit(".", maxsplit=1)[1])
                buckets = [{
                    "key": bucket["key"].split("/taxonomies/")[-1].rstrip("/"),
                    "doc_count": bucket["doc_count"]
                } for bucket in
                    buckets if level == bucket_level(bucket)]
                if buckets:
                    buckets_by_slug = {b["key"].split("/", maxsplit=1)[1]: b for b in buckets}
                    taxonomy_code = buckets[0]["key"].split("/", maxsplit=1)[0]
                    taxonomy_terms = db.session.query(TaxonomyTerm.extra_data,
                                                      TaxonomyTerm.slug).join(Taxonomy).filter(
                        Taxonomy.code == taxonomy_code,
                        TaxonomyTerm.slug.in_(buckets_by_slug.keys()))
                    for extra_data, slug in taxonomy_terms:
                        buckets_by_slug[slug]["key_as_string"] = get_language_aware_title(
                            extra_data, fallback_language=fallback_language)

                aggs[aggs_key]["sterms#links"]["buckets"] = buckets

        return serializer(*args, search_result=search_result, **kwargs)

    def get_language_aware_title(extra_data, fallback_language="en"):
        lang = get_locale()
        title = extra_data["title"]
        local_title = title.get(lang)
        fallback_title = title.get(fallback_language)
        if local_title:
            return local_title
        if fallback_title:
            return fallback_title
        return list(title.values())[0]

    return search
