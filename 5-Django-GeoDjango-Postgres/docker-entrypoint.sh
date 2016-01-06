#!/bin/bash

until nc -z db 5432; do
    echo "$(date) - waiting for postgres..."
    sleep 1
done

echo Running migrations
cd /app && python manage.py migrate                  # Apply database migrations
# cd /src && python manage.py collectstatic --noinput  # Collect static files

echo Starting runserver
cd /app && python manage.py runserver 0.0.0.0:8000
