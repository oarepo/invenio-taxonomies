from collections import Counter

from flask_taxonomies.proxies import current_flask_taxonomies
from flask_taxonomies.term_identification import TermIdentification
from flatten_json import unflatten_list
from invenio_db import db
from slugify import slugify


def import_taxonomy(taxonomy_file, int_conversions, str_args, bool_args, drop):
    data = extract_data(taxonomy_file)

    taxonomy_header, row = read_block(data, 0)
    taxonomy_data, row = read_block(data, row)

    taxonomy = create_update_taxonomy(taxonomy_header, drop)
    create_update_terms(taxonomy, taxonomy_data, int_conversions, str_args, bool_args)


def extract_data(taxonomy_file):
    from openpyxl import load_workbook
    wb = load_workbook(filename=taxonomy_file)
    ws = wb.active
    data = list(ws.rows)
    return data


def create_update_terms(taxonomy, taxonomy_data, int_conversions, str_args, bool_args):
    stack = [taxonomy]
    for term_dict in convert_data_to_dict(taxonomy_data, int_conversions, str_args, bool_args):
        level = int(term_dict.pop('level'))
        slug = term_dict.pop('slug')
        while level < len(stack):
            stack.pop()
        if not slug:
            slug = slugify(next(filter(lambda x: x['lang'] == 'cs', term_dict['title']))['value'])

        # term = taxonomy.get_term(slug)
        identification = TermIdentification(taxonomy=taxonomy, slug=slug)
        term = identification.term_query(
            session=db.session).one_or_none()
        if term:
            # term.update(term_dict)
            current_flask_taxonomies.update_term(identification, extra_data=term_dict)
        else:
            # term = stack[-1].create_term(slug=slug, extra_data=term_dict)
            current_flask_taxonomies.create_term(identification, extra_data=term_dict)
        # stack.append(term)
    db.session.commit()


def create_update_taxonomy(data, drop):
    tax_dict = next(convert_data_to_dict(data))
    if 'code' not in tax_dict:
        raise ValueError('Taxonomy does not contain "code"')
    code = tax_dict.pop('code')
    taxonomy = current_flask_taxonomies.get_taxonomy(code, fail=False)
    # taxonomy = Taxonomy.get(code=code)  # TODO: změnit na nové
    if taxonomy and drop:
        current_flask_taxonomies.delete_taxonomy(taxonomy)
        taxonomy = None

    if taxonomy:
        merged_dict = taxonomy.extra_data
        merged_dict.update(tax_dict)
        # taxonomy.update(extra_data=merged_dict)
        current_flask_taxonomies.update_taxonomy(taxonomy, merged_dict)
    else:
        # taxonomy = Taxonomy.create_taxonomy(code, tax_dict) # TODO: změnit na nové
        current_flask_taxonomies.create_taxonomy(code, extra_data=tax_dict)
    db.session.commit()
    return taxonomy


def convert_data_to_dict(data, int_conversions={}, str_args={}, bool_args={}):
    header = [x.split() if x else None for x in data[0]]
    for block in read_data_blocks(data[1:]):
        ret = {}
        counter = Counter()
        for block_row in block:
            converted_row = {}
            for arridx, prop_path, val in zip(range(0, len(header)), header, block_row):
                if not prop_path:
                    continue
                if ' '.join(prop_path) in int_conversions:
                    val = int(val) if val else None
                elif ' '.join(prop_path) in str_args:
                    val = val if val else ""
                elif ' '.join(prop_path) in bool_args:
                    if val != '':
                        val = val == 'True'
                    else:
                        continue
                flattened_path = []
                for item in prop_path:
                    if "@" in item:
                        flattened_path.append(item[1:])
                        key = "_".join(prop_path)
                        flattened_path.append(str(counter[key]))
                        counter.update({key: 1})
                    else:
                        flattened_path.append(item)
                converted_row["_".join(flattened_path)] = val
            converted_row = {k: v for k, v in converted_row.items() if len(v) > 0}
            ret.update(converted_row)
        yield unflatten_list(ret)


def piecewise_merge(target, source, list_update):
    if isinstance(target, list):
        list_update(target, source)
        return target
    elif isinstance(target, dict):
        for k, v in source.items():
            target[k] = piecewise_merge(target.get(k), v, list_update)
    else:
        if target and source:
            raise Exception(f'Trying to override {target} with {source}')
        if target:
            return target
        return source


def read_data_blocks(data):
    ret = []
    for row in data:
        if row[0]:
            if ret:
                yield ret
                ret = []
        ret.append(row)
    if ret:
        yield ret


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
