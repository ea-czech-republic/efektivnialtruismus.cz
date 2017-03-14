#!/usr/bin/env bash

source bin/development-env.sh && \
/usr/bin/python -m venv .venv --copies && \
source .venv/bin/activate && \
pip install -r requirements.txt && \
cd website && \
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py createsuperuser && \
python manage.py runserver
