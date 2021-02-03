from datetime import datetime

from oarepo_taxonomies.unflatten import unflatten, convert_to_list


def test_unflatten_list():
    dict_ = {
        'level': '2',
        'slug': 'O_historie',
        'title_cs': 'Historie',
        'AKVO': '7105V021',
        'aliases_0': 'Historie - bohemistika',
        'aliases_1': 'Historie - Španělský jazyk a literatura',
        'aliases_2': 'Historie - Archivnictví',
        'aliases_3': 'Historie - Anglická a americká literatura',
        'aliases_4': 'Historie - Bohemistika',
        'aliases_5': 'Historie - Archeologie',
        'aliases_6': 'Historie - anglický jazyk a literatura',
        'aliases_7': 'Historie - Anglický jazyk a literatura',
        'aliases_8': 'Historie - Německý jazyk a literatura',
        'aliases_9': 'Historie - španělský jazyk a literatura',
        'aliases_10': 'Historie - francouzský jazyk a literatura',
        'aliases_11': 'Historie - archivnictví',
        'aliases_12': 'Historie - archeologie',
        'aliases_13': 'Historie - německý jazyk a literatura'
    }
    t0 = datetime.now()
    res = unflatten(dict_)
    assert res == {
        'AKVO': '7105V021',
        'aliases': {
            '0': 'Historie - bohemistika',
            '1': 'Historie - Španělský jazyk a literatura',
            '10': 'Historie - francouzský jazyk a literatura',
            '11': 'Historie - archivnictví',
            '12': 'Historie - archeologie',
            '13': 'Historie - německý jazyk a literatura',
            '2': 'Historie - Archivnictví',
            '3': 'Historie - Anglická a americká literatura',
            '4': 'Historie - Bohemistika',
            '5': 'Historie - Archeologie',
            '6': 'Historie - anglický jazyk a literatura',
            '7': 'Historie - Anglický jazyk a literatura',
            '8': 'Historie - Německý jazyk a literatura',
            '9': 'Historie - španělský jazyk a literatura'
        },
        'level': '2',
        'slug': 'O_historie',
        'title': {'cs': 'Historie'}
    }
    print(datetime.now() - t0)


def test_convert_to_list():
    input = {
        'AKVO': '7105V021',
        'aliases': {
            '0': 'Historie - bohemistika',
            '1': 'Historie - Španělský jazyk a literatura',
            '10': 'Historie - francouzský jazyk a literatura',
            '11': 'Historie - archivnictví',
            '12': 'Historie - archeologie',
            '13': 'Historie - německý jazyk a literatura',
            '2': 'Historie - Archivnictví',
            '3': 'Historie - Anglická a americká literatura',
            '4': 'Historie - Bohemistika',
            '5': 'Historie - Archeologie',
            '6': 'Historie - anglický jazyk a literatura',
            '7': 'Historie - Anglický jazyk a literatura',
            '8': 'Historie - Německý jazyk a literatura',
            '9': 'Historie - španělský jazyk a literatura'
        },
        'level': '2',
        'slug': 'O_historie',
        'title': {'cs': 'Historie'}
    }
    t0 = datetime.now()
    res = convert_to_list(input)
    assert res == {
        'AKVO': '7105V021',
        'aliases': ['Historie - bohemistika',
                    'Historie - Španělský jazyk a literatura',
                    'Historie - Archivnictví',
                    'Historie - Anglická a americká literatura',
                    'Historie - Bohemistika',
                    'Historie - Archeologie',
                    'Historie - anglický jazyk a literatura',
                    'Historie - Anglický jazyk a literatura',
                    'Historie - Německý jazyk a literatura',
                    'Historie - španělský jazyk a literatura',
                    'Historie - francouzský jazyk a literatura',
                    'Historie - archivnictví',
                    'Historie - archeologie',
                    'Historie - německý jazyk a literatura'],
        'level': '2',
        'slug': 'O_historie',
        'title': {'cs': 'Historie'}
    }
    print(datetime.now() - t0)


def test_convert_to_list_2():
    input = {
        'AKVO': '7105V021',
        'aliases': {
            '1': 'Historie - Španělský jazyk a literatura',
            '10': 'Historie - francouzský jazyk a literatura',
            '11': 'Historie - archivnictví',
            '12': 'Historie - archeologie',
            '13': 'Historie - německý jazyk a literatura',
            '2': 'Historie - Archivnictví',
            '3': 'Historie - Anglická a americká literatura',
            '4': 'Historie - Bohemistika',
            '5': 'Historie - Archeologie',
            '6': 'Historie - anglický jazyk a literatura',
            '7': 'Historie - Anglický jazyk a literatura',
            '8': 'Historie - Německý jazyk a literatura',
            '9': 'Historie - španělský jazyk a literatura'
        },
        'level': '2',
        'slug': 'O_historie',
        'title': {'cs': 'Historie'}
    }
    t0 = datetime.now()
    res = convert_to_list(input)
    assert res == {
        'AKVO': '7105V021',
        'aliases': {
            '1': 'Historie - Španělský jazyk a literatura',
            '10': 'Historie - francouzský jazyk a literatura',
            '11': 'Historie - archivnictví',
            '12': 'Historie - archeologie',
            '13': 'Historie - německý jazyk a literatura',
            '2': 'Historie - Archivnictví',
            '3': 'Historie - Anglická a americká literatura',
            '4': 'Historie - Bohemistika',
            '5': 'Historie - Archeologie',
            '6': 'Historie - anglický jazyk a literatura',
            '7': 'Historie - Anglický jazyk a literatura',
            '8': 'Historie - Německý jazyk a literatura',
            '9': 'Historie - španělský jazyk a literatura'
        },
        'level': '2',
        'slug': 'O_historie',
        'title': {'cs': 'Historie'}
    }
    print(datetime.now() - t0)


def test_convert_to_list_3():
    input = {
        'AKVO': '7105V021',
        'aliases': {
            '0': 'Historie - bohemistika',
            '1': 'Historie - Španělský jazyk a literatura',
            '10': 'Historie - francouzský jazyk a literatura',
            '11': 'Historie - archivnictví',
            '12': 'Historie - archeologie',
            '13': 'Historie - německý jazyk a literatura',
            '2': 'Historie - Archivnictví',
            'p': 'Historie - Anglická a americká literatura',
            '4': 'Historie - Bohemistika',
            '5': 'Historie - Archeologie',
            '6': 'Historie - anglický jazyk a literatura',
            '7': 'Historie - Anglický jazyk a literatura',
            '8': 'Historie - Německý jazyk a literatura',
            '9': 'Historie - španělský jazyk a literatura'
        },
        'level': '2',
        'slug': 'O_historie',
        'title': {'cs': 'Historie'}
    }
    t0 = datetime.now()
    res = convert_to_list(input)
    print(datetime.now() - t0)
    assert res == {
        'AKVO': '7105V021',
        'aliases': {
            '12': 'Historie - archeologie',
            '13': 'Historie - německý jazyk a literatura',
            '2': 'Historie - Archivnictví',
            '4': 'Historie - Bohemistika',
            '5': 'Historie - Archeologie',
            '6': 'Historie - anglický jazyk a literatura',
            '7': 'Historie - Anglický jazyk a literatura',
            '8': 'Historie - Německý jazyk a literatura',
            '9': 'Historie - španělský jazyk a literatura',
            'p': 'Historie - Anglická a americká literatura'
        },
        'level': '2',
        'slug': 'O_historie',
        'title': {'cs': 'Historie'}
    }
