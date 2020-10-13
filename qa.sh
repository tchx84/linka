#!/usr/bin/env bash

python3 -m pytest -s tests/tests.py

pycodestyle src/*.py tests/*.py
pyflakes src/*.py tests/*.py
