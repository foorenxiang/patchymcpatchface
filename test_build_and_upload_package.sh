#!/usr/bin/env bash

./pytest.sh
rm -rf dist
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*

# python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps patchymcpatchface