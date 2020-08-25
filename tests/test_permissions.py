import json as json_

from sqlalchemy_utils.types.json import json

from tests.helpers import login


def test_taxonomy_list(permission_client, taxonomy):
    client = permission_client
    taxonomies = client.get('/2.0/taxonomies/')
    assert taxonomies.status_code == 200

    assert json.loads(taxonomies.data) == [{
        'code': 'test_taxonomy',
        'links': {
            'self':
                'http://127.0.0.1:5000/2.0/taxonomies/test_taxonomy/'
        },
        'title': {
            'cs': 'test_taxonomy', 'en': 'test_taxonomy'
        }
    }]


def test_create_update_delete_taxonomy(permission_client, test_users):
    client = permission_client
    content = json_.dumps({"title": "Test taxonomy"}, ensure_ascii=False)
    taxonomy = client.put('/2.0/taxonomies/test', data=content,
                          content_type='application/json')
    assert taxonomy.status_code == 403

    # login
    login(client, test_users[0])

    # create
    taxonomy = client.put('/2.0/taxonomies/test', data=content,
                          content_type='application/json')

    assert taxonomy.status_code == 201

    taxonomy_list = client.get('/2.0/taxonomies/', content_type='application/json')

    assert taxonomy_list.json[0]["code"] == "test"
    assert taxonomy_list.json[0]["title"] == "Test taxonomy"

    # update
    content = json_.dumps({"title": "Test taxonomy updated"}, ensure_ascii=False)
    taxonomy = client.put('/2.0/taxonomies/test', data=content,
                          content_type='application/json')

    assert taxonomy.status_code == 200

    taxonomy_list = client.get('/2.0/taxonomies/', content_type='application/json')

    assert taxonomy_list.json[0]["code"] == "test"
    assert taxonomy_list.json[0]["title"] == "Test taxonomy updated"

    # delete
    taxonomy = client.delete('/2.0/taxonomies/test', content_type='application/json')

    assert taxonomy.status_code == 204

    taxonomy_list = client.get('/2.0/taxonomies/', content_type='application/json')

    assert taxonomy_list.json == []


def test_create_update_delete_taxonomy_term(permission_client, test_users, taxonomy):
    client = permission_client
    content = json_.dumps({"title": "Test term"}, ensure_ascii=False)

    # create without login
    term = client.put('/2.0/taxonomies/test_taxonomy/term', data=content,
                      content_type='application/json')
    assert term.status_code == 403

    # login
    login(client, test_users[0])

    # create
    term = client.put('/2.0/taxonomies/test_taxonomy/term', data=content,
                      content_type='application/json')

    assert term.status_code == 201

    res_term = client.get('/2.0/taxonomies/test_taxonomy/term',
                          content_type='application/json')

    assert res_term.json["title"] == "Test term"

    # update
    content = json_.dumps({"title": "Test term updated"}, ensure_ascii=False)
    term = client.put('/2.0/taxonomies/test_taxonomy/term', data=content,
                      content_type='application/json')

    assert term.status_code == 200

    res_term = client.get('/2.0/taxonomies/test_taxonomy/term',
                          content_type='application/json')

    assert res_term.json["title"] == "Test term updated"

    # delete
    term = client.delete('/2.0/taxonomies/test_taxonomy/term',
                         content_type='application/json')

    assert term.status_code == 200

    res_term = client.get('/2.0/taxonomies/test_taxonomy/term',
                          content_type='application/json')

    assert res_term.status_code == 410
