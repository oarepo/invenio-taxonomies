def taxonomy_term_facet(field, order='desc', size=100):
    return {
            "nested": {
                "path": field
            },
            "aggs": {
                "links": {
                    "terms": {
                        "field": f"{field}.links.self",
                        'size': size,
                        "order": {"_count": order}
                    }
                }
            }
        }