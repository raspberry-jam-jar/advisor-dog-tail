#!/bin/sh
flake8 . &&
black --check . &&
python scripts/travis/wait_for_postgres.py &&
pytest
