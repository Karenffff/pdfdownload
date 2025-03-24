#!/bin/bash
pip install -r requirements.txt
playwright install
playwright install-deps
python manage.py migrate
python manage.py collectstatic --noinput
