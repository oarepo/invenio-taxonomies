import json
from link_header import parse


def test_create_taxonomy(app, client, tax_url):
    print(client.get(tax_url).data)
    assert client.get(tax_url).json == []

    resp = client.put(tax_url + 'test', data='{}', content_type='application/json')
    assert resp.status_code == 201
    created_link = parse(resp.headers['Link']).links_by_attr_pairs([('rel', 'self')])[0].href

    assert client.get(tax_url).json == [{
        'code': 'test',
        'links': {
            'self': 'http://127.0.0.1:5000/2.0/taxonomies/test/'
        }
    }]


def test_create_term(app, client, tax_url):
    client.put(tax_url + 'test', data='{}', content_type='application/json')
    client.put(tax_url + 'test/a', data=json.dumps({'title': 'a'}), content_type='application/json')
    assert client.get(tax_url + 'test/a').json == {
        'links': {
            'self': 'http://127.0.0.1:5000/2.0/taxonomies/test/a'
        },
        'title': 'a'
    }
