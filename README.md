# oarepo-taxonomies
Wrapper that connect Flask-Taxonomies with Invenio.

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]
[![image][8]][9]

  [image]: https://img.shields.io/travis/oarepo/oarepo-taxonomies.svg
  [1]: https://travis-ci.org/oarepo/oarepo-taxonomies
  [2]: https://img.shields.io/coveralls/oarepo/oarepo-taxonomies.svg
  [3]: https://coveralls.io/r/oarepo/oarepo-taxonomies
  [4]: https://img.shields.io/github/tag/oarepo/oarepo-taxonomies.svg
  [5]: https://github.com/oarepo/oarepo-taxonomies/releases
  [6]: https://img.shields.io/pypi/dm/oarepo-taxonomies.svg
  [7]: https://pypi.python.org/pypi/oarepo-taxonomies
  [8]: https://img.shields.io/github/license/oarepo/oarepo-taxonomies.svg
  [9]: https://github.com/oarepo/oarepo-taxonomies/blob/master/LICENSE
  


## Installation

The package is installed classically via the PyPi repository:

`pip install oarepo-taxonomies`

The database is initialized using the management task:

`invenio taxonomies init`

## Quick start

All functionality is provided by flask-taxonomies. For more details see: 
[flask-taxonomies](https://pypi.org/project/flask-taxonomies/7.0.0a13/).

In addition, this package adds the ability to import and export taxonomies using Excel files (* .xlsx)
and can dereference a reference to a taxonomy in an invenio record.

### Import from Excel

Importing from Excel is handled by the management task:

`invenio taxonomies import [OPTIONS] TAXONOMY_FILE`

Options:  
  --int TEXT  
  --str TEXT  
  --bool TEXT  
  --drop / --no-drop  
  --help
  
where:
* `TAXONOMY FILE` is path to the xlsx file (older xls file is not supported)
* `--int, --str, --bool` options are repeatable options and determine data type
* `--drop/--no-drop` Specifies whether the old taxonomy should be removed from the database when we import a
 taxonomy with the same **taxonomy code**.
 
#### Structure of Excel file

**Blocks**

Excel must contain two blocks. The first block contains taxonomy information and must contain one mandatory code column
(taxonomy identifier). Indeed, it can contain other user data (eg. title or description). 

The second block must be
separated from the first by a blank line and must contain two mandatory columns, **level** and **slug**, in exactly
 that order. The other columns are optional.
 
**Nested JSON**  
Taxonomies are internally represented as JSON, which can be nested. Excel spreadsheet is inherently linear and can not
store nested data. However, oarepo-taxonomies support nested JSON. Each value in a nested JSON has its own unique
address. Each JSON level is separated by an underscore, so each branched JSON can be transformed to linear as follows.

Nested:
```json
{
    "a": 1,
    "b": 2,
    "c": [{"d": [2, 3, 4], "e": [{"f": 1, "g": 2}]}]
}
```

Linear:
```json
{"a": 1,
 "b": 2,
 "c_0_d_0": 2,
 "c_0_d_1": 3,
 "c_0_d_2": 4,
 "c_0_e_0_f": 1,
 "c_0_e_0_g": 2
}
```

According to the same pattern, headings can be created in Excel and the data is transformed into a nested form.
 
**Level order**

Taxonomies are tree structures that are also not linear and cannot be transferred to an Excel spreadsheet environment.
Therefore, the sort order goes from root to the lowest child. Root (Taxonomy) -> level 1 first child - ... last
level all children, level 1 second offspring ... etc.

**Excel example**

| code   | title_cs | title_en       |                |
|--------|----------|----------------|----------------|
| cities | Města    | Cities         |                |
|        |          |                |                |
| level  | slug     |       title_cs |       title_en |
| 1      | eu       |         Evropa |         Europe |
| 2      | cz       | Česko          | Czechia        |
| 3      | prg      | Praha          | Prague         |
| 3      | brn      | Brno           | Brno           |
| 2      | de       | Německo        | Germany        |
| 3      | ber      | Berlín         | Berlin         |
| 3      | mun      | Mnichov        | Munich         |
| 2      | gb       | Velká Británie | United Kingdom |
| 3      | lon      | Londýn         | London         |
| 3      | man      | Manchester     | Manchester     |

The resulting json for the taxonomy will take the following form:

```json
{
  "code": "cities",
  "title": {
    "cs": "Města",
    "en": "Citites"
  }
}
```

and for individual Taxonomy Term:

```json
{
  "code": "Praha",
  "title": {
    "cs": "Praha",
    "en": "Prague"
  }
}
```

and tree structure:
<pre>
cities  
└-eu  
  |--cz  
  |  |--prg  
  |  └--brn  
  |--de  
  |  |--ber   
  |  └--mun  
  └--gb  
     |--lon   
     └--man      
</pre>  

### Export to Excel

Excel export is created using a management task `invenio taxonomies export TAXONOMY_CODE`.

An xlsx and csv file is created in the current folder where the task was run.

### Marshmallow
```python
from marshmallow import Schema
from marshmallow.fields import Nested
from oarepo_taxonomies.marshmallow import TaxonomyField


class UserSchema(Schema):
    taxonomy = Nested(TaxonomyField)
    # ... user data

random_user_data = {
        "created_at": "2014-08-11T05:26:03.869245",
        "email": "ken@yahoo.com",
        "name": "Ken",
        "taxonomy": {
            "links": {
                "self": "http://localhost/api/2.0/taxonomies/test_taxonomy/a/b"
            }
        }
    }
schema = TaxonomyField()   
json = schema.load(random_user_data)

```

The Marshmallow module serialize Taxonomy and dereference reference from links/self.
The module provides the Marshmallo subschema `TaxonomyField`, which can be freely used in the user schema.
TaxonomyField receives any user data and checks if the user data is JSON/dict or string.

If the user data is JSON/dict, then it looks for the links/self and fetch data form taxonomy.
The data provided by the user and are also in the taxonomy are overwritten. Other user data are kept.

If the user data is of type string, Marshmallow will try to find a link to the taxonomy and return
its entire representation.