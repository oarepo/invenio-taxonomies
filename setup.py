# -*- coding: utf-8 -*-


"""Wrapper that connect flask-taxonomies with Invenio"""
import os
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

tests_require = [
    'pytest',
    'pytest-cov',
    'oarepo==3.3.26',
]
extras_require = {
    "tests": tests_require
}

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'flask-taxonomies>=7.0.0a17',
    'flatten_json>=0.1.7,<1.0.0,!=0.1.8',
    'openpyxl>=3.0.4,<4.0.0',
    'oarepo-mapping-includes>=1.2.0,<2.0.0',
    'oarepo-references[validate]>=1.8.3,<2.0.0',
    'deepmerge>=0.1.0',
    'boltons>=20.0.0'
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('oarepo_taxonomies', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='oarepo_taxonomies',
    version=version,
    description=__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='oarepo taxonomies',
    license='MIT',
    author='Daniel Kopecký',
    author_email='Daniel.Kopecky@techlib.cz',
    url='https://github.com/oarepo/oarepo-taxonomies',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'flask.commands': [
            'taxonomies = oarepo_taxonomies.cli:taxonomies',
        ],
        'invenio_base.api_apps': [
            'taxonomies = oarepo_taxonomies.ext:OarepoTaxonomies'
        ],
        'invenio_base.apps': [
            'taxonomies = oarepo_taxonomies.ext:OarepoTaxonomies'
        ],
        'invenio_jsonschemas.schemas': [
            'oarepo_taxonomies = oarepo_taxonomies.jsonschemas'
        ],
        "oarepo_mapping_handlers": [
            "taxonomy-term = oarepo_taxonomies.mappings:taxonomy_term"
        ],
        'invenio_celery.tasks': [
            'oarepo_taxonomies = oarepo_taxonomies.tasks'
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
)
