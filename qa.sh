#!/usr/bin/env bash

python3 -m pytest -s tests/service.py

pycodestyle app/*.py tests/*.py
pyflakes app/*.py tests/*.py
