#!/bin/sh

# entrypoint script for docker container
python manage.py makemigrations
python manage.py migrate

# runserver
python manage.py runserver 0.0.0.0:8000
