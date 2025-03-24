#!/bin/bash
pip install -r requirements.txt
playwright install --with-deps
playwright install-deps
python manage.py migrate
python manage.py collectstatic --noinput
