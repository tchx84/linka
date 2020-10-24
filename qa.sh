#!/usr/bin/env bash

python3 -m pytest -s tests/service.py && \

pycodestyle app/*.py cli/*.py tests/*.py && \
pyflakes app/*.py cli/*.py tests/*.py
