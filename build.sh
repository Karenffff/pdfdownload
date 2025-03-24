#!/bin/bash
pip install -r requirements.txt
apt-get update && apt-get install -y libpango-1.0-0 libcairo2 libjpeg62-turbo libpangocairo-1.0-0 libgdk-pixbuf2.0-0
python manage.py migrate
python manage.py collectstatic --noinput
