from oarepo_taxonomies.tasks import apptask


def test_current_app():
    r = apptask.delay()
    print(r.result)
