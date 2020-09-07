from celery import shared_task
from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.term_identification import TermIdentification
from oarepo_references.proxies import current_references

from oarepo_taxonomies.marshmallow import get_slug_from_link


@shared_task
def async_reference_changed(old_url, new_url):
    current_references.reference_changed(old=old_url, new=new_url)


@shared_task
def async_reference_content_changed(ref_obj, ref_url=None, ref_uuid=None):
    current_references.reference_content_changed(ref_obj, ref_url=ref_url, ref_uuid=ref_uuid)


@shared_task
def unlock_term(*args, **kwargs):
    term_url = kwargs.get("url")
    if not term_url:
        return
    _unlock_term(term_url)


def _unlock_term(term_url):
    slug, taxonomy_code = get_slug_from_link(term_url)
    term_identification = TermIdentification(taxonomy=taxonomy_code, slug=slug)
    term_list = list(current_flask_taxonomies.filter_term(term_identification))
    if not term_list:
        return
    term = term_list[0]
    busy_count_0 = term.busy_count
    current_flask_taxonomies.unmark_busy([term.id])
    assert term.busy_count < busy_count_0
