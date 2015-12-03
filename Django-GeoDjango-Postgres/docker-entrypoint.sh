#!/bin/bash

echo Running migrations
cd /app && python manage.py migrate                  # Apply database migrations
# cd /src && python manage.py collectstatic --noinput  # Collect static files

echo Starting runserver
cd /app && python manage.py runserver 0.0.0.0:8000
