#!/usr/bin/env bash

pyflakes app cli tests tools && \
black --check app cli tests tools && \
python3 -m pytest -s -vv tests/service.py
