import os
import pathlib
from pathlib import Path

import pytest
from flask_taxonomies.proxies import current_flask_taxonomies

from oarepo_taxonomies.import_export import export_taxonomy, import_taxonomy
from oarepo_taxonomies.import_export.export_excel import get_taxonomy_header_dict, \
    get_taxonomy_terms_list


def test_export_taxonomy(app, db):
    file_path = pathlib.Path(__file__).parent.absolute()
    data_path = file_path / "data" / "licenses_v2.xlsx"
    str_path = str(data_path)
    import_taxonomy(str_path)

    csv_path, excel_path = export_taxonomy("licenses")

    assert Path(csv_path).is_file()
    assert Path(excel_path).is_file()
    os.remove(csv_path)
    os.remove(excel_path)


def test_get_taxonomy_header_dict(app, db, taxonomy):
    res = get_taxonomy_header_dict(taxonomy)
    assert res == {
        'code': 'test_taxonomy',
        'title_cs': 'test_taxonomy',
        'title_en': 'test_taxonomy'
    }


def test_get_taxonomy_terms_list(app, db):
    file_path = pathlib.Path(__file__).parent.absolute()
    data_path = file_path / "data" / "licenses_v2.xlsx"
    str_path = str(data_path)
    import_taxonomy(str_path)

    taxonomy = current_flask_taxonomies.get_taxonomy("licenses")
    first_level = current_flask_taxonomies.list_taxonomy(taxonomy, levels=1).all()
    res = get_taxonomy_terms_list(first_level)
    assert res[0]["level"] == 1
    assert res[1]["level"] == 2
    assert res[2]["level"] == 3
    assert res[3]["level"] == 3
    assert res[8]["level"] == 2


@pytest.fixture()
def taxonomy_header():
    return {
        'code': 'test_taxonomy',
        'title_cs': 'test_taxonomy',
        'title_en': 'test_taxonomy'
    }


@pytest.fixture()
def flattened_ls():
    return [{
        'level': 1,
        'slug': 'cc',
        'title_cs': 'Licence Creative Commons',
        'title_en': 'License Creative Commons'
    },
        {
            'level': 2,
            'slug': '1-0',
            'title_cs': 'verze 1.0 Obecná licence',
            'title_en': 'version 1.0 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by/1.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by/1.0/',
            'slug': '1-by',
            'title_cs': 'Creative Commons Uveďte původ 1.0 Obecná licence',
            'title_en': 'Creative Commons Attribution 1.0 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc/1.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc/1.0/',
            'slug': '1-by-nc',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte komerčně 1.0 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-NonCommercial 1.0 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-sa/1.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-sa/1.0/',
            'slug': '1-by-nc-sa',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte dílo '
                        'komerčně-Zachovejte licenci 1.0 Obecná licence',
            'title_en': 'Creative Commons Attribution-NonCommercial-ShareAlike 1.0 '
                        'Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nd/1.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nd/1.0/',
            'slug': '1-by-nd',
            'title_cs': 'Creative Commons Uveďte původ-Nezpracovávejte 1.0 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-NoDerivs 1.0 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nd-nc/1.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nd-nc/1.0/',
            'slug': '1-by-nd-nc',
            'title_cs': 'Creative Commons Uveďte původ-Nezpracovávejte-Neužívejte '
                        'komerčně 1.0 Obecná licence',
            'title_en': 'Creative Commons Attribution-NoDerivs-NonCommercial 1.0 Generic '
                        'License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-sa/1.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-sa/1.0/',
            'slug': '1-by-sa',
            'title_cs': 'Creative Commons Uveďte původ-Zachovejte licenci 1.0 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-ShareAlike 1.0 Generic License'
        },
        {
            'level': 2,
            'slug': '2-0',
            'title_cs': 'verze 2.0 Obecná licence',
            'title_en': 'version 2.0 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by/2.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by/2.0/',
            'slug': '2-by',
            'title_cs': 'Creative Commons Uveďte původ 2.0 Obecná licence',
            'title_en': 'Creative Commons Attribution 2.0 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc/2.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc/2.0/',
            'slug': '2-by-nc',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte komerčně 2.0 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-NonCommercial 2.0 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-nd/2.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-nd/2.0/',
            'slug': '2-by-nc-nd',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte '
                        'komerčně-Nezpracovávejte 2.0 Obecná licence',
            'title_en': 'Creative Commons Attribution-NonCommercial-NoDerivs 2.0 Generic '
                        'License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-sa/2.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-sa/2.0/',
            'slug': '2-by-nc-sa',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte dílo '
                        'komerčně-Zachovejte licenci 2.0 Obecná licence',
            'title_en': 'Creative Commons Attribution-NonCommercial-ShareAlike 2.0 '
                        'Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nd/2.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nd/2.0/',
            'slug': '2-by-nd',
            'title_cs': 'Creative Commons Uveďte původ-Nezpracovávejte 2.0 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-NoDerivs 2.0 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-sa/2.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-sa/2.0/',
            'slug': '2-by-sa',
            'title_cs': 'Creative Commons Uveďte původ-Zachovejte licenci 2.0 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-ShareAlike 2.0 Generic License'
        },
        {
            'level': 2,
            'slug': '2-5',
            'title_cs': 'verze 2.5 Obecná licence',
            'title_en': 'version 2.5 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by/2.5/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by/2.5/',
            'slug': '2-5-by',
            'title_cs': 'Creative Commons Uveďte původ 2.5 Obecná licence',
            'title_en': 'Creative Commons Attribution 2.5 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc/2.5/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc/2.5/',
            'slug': '2-5-by-nc',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte komerčně 2.5 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-NonCommercial 2.5 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-nd/2.5/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-nd/2.5/',
            'slug': '2-5-by-nc-nd',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte '
                        'komerčně-Nezpracovávejte 2.5 Obecná licence',
            'title_en': 'Creative Commons Attribution-NonCommercial-NoDerivs 2.5 Generic '
                        'License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-sa/2.5/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-sa/2.5/',
            'slug': '2-5-by-nc-sa',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte dílo '
                        'komerčně-Zachovejte licenci 2.5 Obecná licence',
            'title_en': 'Creative Commons Attribution-NonCommercial-ShareAlike 2.5 '
                        'Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nd/2.5/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nd/2.5/',
            'slug': '2-5-by-nd',
            'title_cs': 'Creative Commons Uveďte původ-Nezpracovávejte 2.5 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-NoDerivs 2.5 Generic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-sa/2.5/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-sa/2.5/',
            'slug': '2-5-by-sa',
            'title_cs': 'Creative Commons Uveďte původ-Zachovejte licenci 2.5 Obecná '
                        'licence',
            'title_en': 'Creative Commons Attribution-ShareAlike 2.5 Generic License'
        },
        {
            'level': 2,
            'slug': '3-0',
            'title_cs': 'verze 3.0 Česko',
            'title_en': 'version 3.0 Czech Republic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by/3.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by/3.0/cz/',
            'slug': '3-by-cz',
            'title_cs': 'Creative Commons Uveďte autora 3.0 Česko',
            'title_en': 'Creative Commons Attribution 3.0 Czech Republic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc/3.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc/3.0/cz/',
            'slug': '3-by-nc-cz',
            'title_cs': 'Creative Commons Uveďte autora-Neužívejte komerčně 3.0 Česko',
            'title_en': 'Creative Commons Attribution-NonCommercial 3.0 Czech Republic '
                        'License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-nd/3.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-nd/3.0/cz/',
            'slug': '3-by-nc-nd-cz',
            'title_cs': 'Creative Commons Uveďte autora-Neužívejte komerčně-Nezasahujte '
                        'do díla 3.0 Česko',
            'title_en': 'Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Czech '
                        'Republic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-sa/3.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-sa/3.0/cz/',
            'slug': '3-by-nc-sa-cz',
            'title_cs': 'Creative Commons Uveďte autora-Neužívejte komerčně-Zachovejte '
                        'licenci 3.0 Česko',
            'title_en': 'Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Czech '
                        'Republic License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nd/3.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nd/3.0/cz/',
            'slug': '3-by-nd-cz',
            'title_cs': 'Creative Commons Uveďte autora-Nezasahujte do díla 3.0 Česko',
            'title_en': 'Creative Commons Attribution-NoDerivs 3.0 Czech Republic '
                        'License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-sa/3.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-sa/3.0/cz/',
            'slug': '3-by-sa-cz',
            'title_cs': 'Creative Commons Uveďte autora-Zachovejte licenci 3.0 Česko',
            'title_en': 'Creative Commons Attribution-ShareAlike 3.0 Czech Republic '
                        'License'
        },
        {
            'level': 2,
            'slug': '4-0',
            'title_cs': 'verze 4.0 mezinárodní licence',
            'title_en': 'version 4.0 International License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by/4.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by/4.0/',
            'slug': '4-by',
            'title_cs': 'Creative Commons Uveďte původ 4.0 Mezinárodní licence',
            'title_en': 'Creative Commons Attribution 4.0 International License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc/4.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc/4.0/',
            'slug': '4-by-nc',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte komerčně 4.0 '
                        'Mezinárodní licence',
            'title_en': 'Creative Commons Attribution-NonCommercial 4.0 International '
                        'License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-nd/4.0/',
            'slug': '4-by-nc-nd',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte '
                        'komerčně-Nezpracovávejte 4.0 Mezinárodní licence',
            'title_en': 'Creative Commons Attribution-NonCommercial-NoDerivs 4.0 '
                        'International License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nc-sa/4.0/',
            'slug': '4-by-nc-sa',
            'title_cs': 'Creative Commons Uveďte původ-Neužívejte dílo '
                        'komerčně-Zachovejte licenci 4.0 Mezinárodní licence',
            'title_en': 'Creative Commons Attribution-NonCommercial-ShareAlike 4.0 '
                        'International License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-nd/4.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-nd/4.0/',
            'slug': '4-by-nd',
            'title_cs': 'Creative Commons Uveďte původ-Nezpracovávejte 4.0 Mezinárodní '
                        'licence',
            'title_en': 'Creative Commons Attribution-NoDerivs 4.0 International '
                        'License'
        },
        {
            'icon': 'https://licensebuttons.net/l/by-sa/4.0/88x31.png',
            'level': 3,
            'related_uri': 'https://creativecommons.org/licenses/by-sa/4.0/',
            'slug': '4-by-sa',
            'title_cs': 'Creative Commons Uveďte původ-Zachovejte licenci 4.0 '
                        'Mezinárodní licence',
            'title_en': 'Creative Commons Attribution-ShareAlike 4.0 International '
                        'License'
        },
        {
            'level': 1,
            'slug': 'copyright',
            'title_cs': 'Dílo je chráněno podle autorského zákona č. 121/2000 Sb.',
            'title_en': 'This work is protected under the Copyright Act No. 121/2000 '
                        'Coll.'
        },
        {
            'level': 1,
            'slug': 'test-slugify',
            'title_cs': 'test slugify',
            'title_en': 'test slugify'
        }]
