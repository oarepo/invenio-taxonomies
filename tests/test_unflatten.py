from datetime import datetime
from pprint import pprint

from oarepo_taxonomies.unflatten import unflatten, convert_to_list


def test_unflatten():
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


def test_unflatten_2():
    input = {
        'level': '2', 'slug': 'D012046', 'title_cs': 'rehabilitace', 'title_en': 'Rehabilitation',
        'relatedURI_0': 'http://www.medvik.cz/link/D012046',
        'relatedURI_1': 'http://id.nlm.nih.gov/mesh/D012046', 'TreeNumberList_0': 'E02',
        'TreeNumberList_1': 'E02.760', 'TreeNumberList_2': 'E02.760.169',
        'TreeNumberList_3': 'E02.760.169.063', 'TreeNumberList_4': 'E02.760.169.063.500',
        'TreeNumberList_5': 'E02', 'TreeNumberList_6': 'E02.831', 'TreeNumberList_7': 'H02',
        'TreeNumberList_8': 'H02.403', 'TreeNumberList_9': 'H02.403.680',
        'TreeNumberList_10': 'H02.403.680.600', 'TreeNumberList_11': 'N02',
        'TreeNumberList_12': 'N02.421', 'TreeNumberList_13': 'N02.421.784'
    }
    t0 = datetime.now()
    res = unflatten(input)
    print(datetime.now() - t0)
    assert res == {
        'TreeNumberList': {
            '0': 'E02',
            '1': 'E02.760',
            '10': 'H02.403.680.600',
            '11': 'N02',
            '12': 'N02.421',
            '13': 'N02.421.784',
            '2': 'E02.760.169',
            '3': 'E02.760.169.063',
            '4': 'E02.760.169.063.500',
            '5': 'E02',
            '6': 'E02.831',
            '7': 'H02',
            '8': 'H02.403',
            '9': 'H02.403.680'
        },
        'level': '2',
        'relatedURI': {
            '0': 'http://www.medvik.cz/link/D012046',
            '1': 'http://id.nlm.nih.gov/mesh/D012046'
        },
        'slug': 'D012046',
        'title': {'cs': 'rehabilitace', 'en': 'Rehabilitation'}
    }


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


def test_convert_to_list_4():
    input = {
        'TreeNumberList': {
            '0': 'E02',
            '1': 'E02.760',
            '10': 'H02.403.680.600',
            '11': 'N02',
            '12': 'N02.421',
            '13': 'N02.421.784',
            '2': 'E02.760.169',
            '3': 'E02.760.169.063',
            '4': 'E02.760.169.063.500',
            '5': 'E02',
            '6': 'E02.831',
            '7': 'H02',
            '8': 'H02.403',
            '9': 'H02.403.680'
        },
        'level': '2',
        'relatedURI': {
            '0': 'http://www.medvik.cz/link/D012046',
            '1': 'http://id.nlm.nih.gov/mesh/D012046'
        },
        'slug': 'D012046',
        'title': {'cs': 'rehabilitace', 'en': 'Rehabilitation'}
    }
    t0 = datetime.now()
    res = convert_to_list(input)
    print(datetime.now() - t0)
    pprint(res)
    assert res == {
        'TreeNumberList': ['E02',
                           'E02.760',
                           'E02.760.169',
                           'E02.760.169.063',
                           'E02.760.169.063.500',
                           'E02',
                           'E02.831',
                           'H02',
                           'H02.403',
                           'H02.403.680',
                           'H02.403.680.600',
                           'N02',
                           'N02.421',
                           'N02.421.784'],
        'level': '2',
        'relatedURI': ['http://www.medvik.cz/link/D012046',
                       'http://id.nlm.nih.gov/mesh/D012046'],
        'slug': 'D012046',
        'title': {'cs': 'rehabilitace', 'en': 'Rehabilitation'}
    }
