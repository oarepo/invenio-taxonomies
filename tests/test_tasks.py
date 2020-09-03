from oarepo_taxonomies.tasks import sum


def test_task_1(app, db):
    result = sum.delay(2, 2)
    print(sum(2, 2))
    print(result)
    print(result.result)
