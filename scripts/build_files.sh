#!/bin/bash
python3 manage.py makemigrations
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
gunicorn --config gunicorn_config.py project.wsgi:application
