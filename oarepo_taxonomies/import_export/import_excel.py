from flask_taxonomies.models import Taxonomy
from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.term_identification import TermIdentification
from invenio_db import db
from slugify import slugify

from oarepo_taxonomies.unflatten import unflatten_list


def import_taxonomy(taxonomy_file,
                    str_args: tuple = tuple(),
                    int_conversions: tuple = tuple(),
                    bool_args: tuple = tuple(),
                    drop=False,
                    resolve_list=False
                    ):
    data = extract_data(taxonomy_file)

    taxonomy_header, row = read_block(data, 0)
    taxonomy_data, row = read_block(data, row)

    taxonomy = create_update_taxonomy(taxonomy_header, drop)
    create_update_terms(taxonomy, taxonomy_data, str_args, int_conversions, bool_args,
                        resolve_list=resolve_list)


def extract_data(taxonomy_file):
    from openpyxl import load_workbook
    wb = load_workbook(filename=taxonomy_file)
    ws = wb.active
    data = list(ws.rows)
    return data


def get_resolved_list(v):
    if isinstance(v, str) and v.startswith("[") and v.endswith("]"):
        return eval(v)
    return v


def create_update_terms(taxonomy,
                        taxonomy_data,
                        str_args: tuple = tuple(),
                        int_conversions: tuple = tuple(),
                        bool_args: tuple = tuple(),
                        resolve_list=False
                        ):
    stack = [taxonomy]
    for term_dict in convert_data_to_dict(taxonomy_data, str_args=str_args,
                                          int_conversions=int_conversions, bool_args=bool_args):
        if resolve_list:
            term_dict = {k: get_resolved_list(v) for k, v in term_dict.items()}
        level = int(term_dict.pop('level'))
        try:
            slug = term_dict.pop('slug')
        except KeyError:
            slug = None
        while level < len(stack):
            stack.pop()
        if not slug:
            slug = slugify(term_dict["title"]["cs"])
        else:
            slug = slugify(slug)
        last_stack = stack[-1]
        if isinstance(last_stack, Taxonomy):
            identification = TermIdentification(taxonomy=taxonomy, slug=slug)
        else:
            identification = TermIdentification(parent=last_stack, slug=slug)
        term = current_flask_taxonomies.filter_term(identification).one_or_none()
        if term:
            current_flask_taxonomies.update_term(identification, extra_data=term_dict)
            print(f'Term "{identification}" has been updated')
        else:
            term = current_flask_taxonomies.create_term(identification, extra_data=term_dict)
            print(f'Term "{identification}" has been created')
        stack.append(term)
    db.session.commit()


def create_update_taxonomy(data, drop) -> Taxonomy:
    tax_dict = convert_data_to_dict(data)[0]
    if 'code' not in tax_dict:
        raise ValueError('Taxonomy does not contain "code"')
    code = tax_dict.pop('code')
    taxonomy = current_flask_taxonomies.get_taxonomy(code, fail=False)
    if taxonomy and drop:
        current_flask_taxonomies.delete_taxonomy(taxonomy)
        taxonomy = None

    if taxonomy:
        merged_dict = taxonomy.extra_data
        merged_dict.update(tax_dict)
        current_flask_taxonomies.update_taxonomy(taxonomy, merged_dict)
    else:
        taxonomy = current_flask_taxonomies.create_taxonomy(code, extra_data=tax_dict)
    db.session.commit()
    return taxonomy


def convert_data_to_dict(data: list,
                         str_args: tuple = tuple(),
                         int_conversions: tuple = tuple(),
                         bool_args: tuple = tuple()
                         ) -> list:
    """
    Function that translate excel flatten json into standard nested json.

    :param data: List of lists, where each list represent row in excel table.
    :type data: list
    :param str_args:
    :type str_args:
    :param int_conversions:
    :type int_conversions:
    :param bool_args:
    :type bool_args:
    :return: list of nested dictionaries
    :rtype: list
    """
    header = data[0]
    content = data[1:]
    res = []
    for r, row in enumerate(content):
        row_dict = {}
        for c, column in enumerate(row):
            if column:
                if header[c] in str_args:
                    row_dict[header[c]] = str(column)
                elif header[c] in int_conversions:
                    row_dict[header[c]] = int(column)
                elif header[c] in bool_args:
                    row_dict[header[c]] = bool(column)
                else:
                    row_dict[header[c]] = column

        res.append(row_dict)
    return [unflatten_list(x) for x in res]


def read_block(data, startrow):
    """
    The function returns a block of rows with some data in a row.
    A blank line separates the block.
    :param data: Data is a list of tuples, where each tuple represents a row.
     The element for tuple is Cell.
    :param startrow: Starting row, where function finding block.
    :return: Returns a list of lists. The inner list represents columns and the outer row list.
     Cell values are strings.
    """
    ret = []

    def convert(x):
        """
        Function that convert openpyxl Cell to readable value
        """
        if x.value is None:
            return ''
        return str(x.value).strip()

    empty = False
    rowidx = startrow
    starting = True
    heading = [convert(x) for x in data[startrow]]
    heading = [x for x in heading if len(x) > 0]
    columns = len(heading)
    sliced_data = [row[:columns] for row in data]
    for row in sliced_data[startrow:]:
        rowidx += 1
        row = [convert(x) for x in row]
        for c in row:
            if c:
                break
        else:
            if starting:
                continue
            # all values empty
            if empty:
                break
            empty = True
            continue
        ret.append(row)
        empty = False
        starting = False

    return ret, rowidx
