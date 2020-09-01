import logging

from oarepo_references.proxies import current_references

from oarepo_taxonomies.exceptions import DeleteAbortedError

logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


def taxonomy_delete(*args, **kwargs):
    tax = kwargs["taxonomy"]
    url = tax.links().envelope["self"]
    raise_aborted_error(url)


def taxonomy_term_delete(*args, **kwargs):
    term = kwargs["term"]
    url = term.links().envelope["self"]
    raise_aborted_error(url)


def taxonomy_term_update(*args, **kwargs):
    print("taxonomy_term_update", args, kwargs)


def taxonomy_term_moved(*args, **kwargs):
    old_term = kwargs["term"]
    new_term = kwargs["new_term"]
    old_url = old_term.links().envelope["self"]
    new_url = new_term.links().envelope["self"]
    changed_records = current_references.reference_changed(old=old_url, new=new_url)
    logger.debug(f"Changed records: {changed_records}")


def raise_aborted_error(url):
    record_ids, records = get_records(url)
    if records:
        raise DeleteAbortedError(
            f"You cannot delete a taxonomy that is contained in references. First, delete the "
            f"references in these records: {record_ids}")


def get_records(url):
    records = current_references.get_records(url)
    record_ids = [rec.record_id for rec in records]
    return record_ids, records
