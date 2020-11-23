#!/usr/bin/env bash

pyflakes app cli tests && \
black --check app cli tests && \
python3 -m pytest -s tests/service.py
