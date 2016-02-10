#!/bin/bash

until nc -z db 5432; do
    echo "$(date) - waiting for postgres..."
    sleep 1
done

echo Running migrations
exec python manage.py migrate                  # Apply database migrations
# cd /src && python manage.py collectstatic --noinput  # Collect static files

echo Starting uwsg
exec uwsgi --ini /uwsgi.ini

# echo Starting runserver
# python manage.py runserver 0.0.0.0:8000
