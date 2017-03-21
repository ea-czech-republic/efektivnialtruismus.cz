#!/usr/bin/env bash
set -e
set -a

source bin/development-env.sh  # source a file with environment variables

### Prepare Python environment
python3 -m venv .venv --copies  # create a virtual environment
source .venv/bin/activate  # activate the environment
pip install -r requirements.txt  # install all dependencies

# Prepare wagtail app
cd website
python3 manage.py makemigrations
python3 manage.py migrate  # prepare database for all models
python3 manage.py createsuperuser 
python3 manage.py runserver  # runserver on 127.0.0.1:8000
set +a
