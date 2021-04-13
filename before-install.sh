#!/usr/bin/env sh

pip install --upgrade pip setuptools
pip install twine wheel coveralls requirements-builder pip-tools
requirements-builder --level=pypi -e tests setup.py >.travis-release-requirements.in
pip-compile -U --verbose -o .travis-release-requirements.txt .travis-release-requirements.in
cat .travis-release-requirements.txt
