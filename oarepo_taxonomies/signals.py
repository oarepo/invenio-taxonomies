from oarepo_references.proxies import current_references


def taxonomy_delete(*args, **kwargs):
    print("taxonomy_delete", args, kwargs)


def taxonomy_term_update(*args, **kwargs):
    print("taxonomy_term_update", args, kwargs)


def taxonomy_term_moved(*args, **kwargs):
    print("taxonomy_term_update", args, kwargs)


def taxonomy_term_created(*args, **kwargs):
    print("taxonomy_term_update", args, kwargs)


def taxonomy_term_delete(*args, **kwargs):
    print("taxonomy_term_delete", args, kwargs)
