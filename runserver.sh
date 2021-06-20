#!/bin/bash

export DJANGO_SETTINGS_MODULE=myshop.settings.local
exec python manage.py runserver 127.0.0.1:8000
