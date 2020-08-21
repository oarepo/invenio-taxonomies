# -*- coding: utf-8 -*-


"""oarepo OAI-PMH converter."""
import os

from setuptools import find_packages, setup

tests_require = [
    'pytest',
    'pytest-cov'
]
extras_require = {
    "devel": ['oarepo[deploy-es7]>=3.2.1.2', *tests_require],
    "tests": tests_require
}

setup_requires = [
    'pytest-runner>=2.7',
]

install_requires = [
    'flask-taxonomies>= 7.0.0a13',
    'flatten_json>=0.1.7,<1.0.0',
    'openpyxl>=3.0.4,<4.0.0'
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
    # long_description=,
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
        ]
        # TODO: vymyslet napojení na InvenioDB
        # 'invenio_db.models': [
        #     'invenio_oarepo_oai_pmh_harvester = invenio_oarepo_oai_pmh_harvester.models',
        # ],
        # 'invenio_db.alembic': [
        #     'invenio_oarepo_oai_pmh_harvester = invenio_oarepo_oai_pmh_harvester:alembic',
        # ],
        # 'flask.commands': [
        #     'nusl = example.cli:nusl',
        #     'oai = invenio_oarepo_oai_pmh_harvester.cli:oai'
        # ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
)
