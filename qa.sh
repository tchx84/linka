#!/usr/bin/env bash

pyflakes app tests tools && \
black --check app tests tools && \
python3 -m pytest -s -vv tests/service.py
