#!/bin/bash
pip install -r requirements.txt
playwright install --with-deps
python manage.py migrate
python manage.py collectstatic --noinput
