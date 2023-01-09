#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py createsu
python manage.py addcurrencies
python manage.py collectstatic --noinput

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --daemon

nginx -g 'daemon off;'