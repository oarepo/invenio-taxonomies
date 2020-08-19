import csv
import pathlib
from pathlib import Path

from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from flask_taxonomies.proxies import current_flask_taxonomies
from flatten_json import flatten


def export_taxonomy(taxonomy_code: str):
    # get cwd path
    cwd = pathlib.Path().absolute()
    path = str(cwd / f"{taxonomy_code}.csv")

    # get taxonomy flatten dicts (header and content)
    taxonomy = current_flask_taxonomies.get_taxonomy(taxonomy_code)
    first_level_list = current_flask_taxonomies.list_taxonomy(taxonomy, levels=1).all()
    taxonomy_header_dict = get_taxonomy_header_dict(taxonomy)
    taxonomy_terms_list = get_taxonomy_terms_list(first_level_list)

    csv_path = convert_to_csv(path, taxonomy_terms_list)
    excel_path = convert_csv_to_excel(path, taxonomy_header_dict)
    return csv_path, excel_path


def get_taxonomy_header_dict(taxonomy: Taxonomy):
    res = {"code": taxonomy.code}
    res.update(**taxonomy.extra_data)
    return flatten(res)


def get_taxonomy_terms_list(item: list, result=None):
    if result is None:
        result = []
    if isinstance(item, (list, tuple)):
        for term in item:
            get_taxonomy_terms_list(term, result=result)
    if isinstance(item, TaxonomyTerm):
        children = item.children.all()
        if children:
            result.append(get_flatten_dict(item))
            for child in children:
                get_taxonomy_terms_list(child, result=result)
        else:
            result.append(get_flatten_dict(item))
    return result


def get_flatten_dict(term: TaxonomyTerm):
    row_dict = {
        "level": term.level + 1,
        "slug": term.slug.split("/")[-1]
    }
    row_dict.update(**term.extra_data)
    return flatten(row_dict)


def convert_to_csv(path: str, flattened_ls: list):
    with open(path, 'w', newline='') as csvfile:
        fieldnames = create_field_names(flattened_ls)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in flattened_ls:
            writer.writerow(row)
    return path


def create_field_names(flattened_ls: list) -> list:
    field_names = ["level", "slug"]
    for row in flattened_ls:
        for key in row.keys():
            if key not in field_names:
                field_names.append(key)
    return field_names


def convert_csv_to_excel(csv_path: str, taxonomy_header):
    from openpyxl import Workbook

    p = Path(csv_path).parent
    excel_path = p / f"{taxonomy_header['code']}.xlsx"
    wb = Workbook()
    ws = wb.active
    rows = [[key for key in taxonomy_header.keys()], [value for value in taxonomy_header.values()]]
    for row in rows:
        ws.append(row)
    for row in range(2):
        ws.append([])
    with open(csv_path, 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save(str(excel_path))
    return excel_path
