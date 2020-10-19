#!/usr/bin/env bash

DATABASE_URL="sqlite:///./test.db" python3 -m pytest -s tests/service.py && \

pycodestyle app/*.py tests/*.py && \
pyflakes app/*.py tests/*.py
