#!/bin/sh

# اجرای migrate و makemigrations
python manage.py makemigrations
python manage.py migrate

# اجرای سرور جنگو
python manage.py runserver 0.0.0.0:8000
