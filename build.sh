#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install
cd takutail
ls -la
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py import_csv
python manage.py runserver
