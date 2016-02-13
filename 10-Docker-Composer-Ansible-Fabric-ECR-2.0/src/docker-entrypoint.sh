#!/bin/bash

# Wait until postgres is ready
until nc -z db 5432; do
    echo "$(date) - waiting for postgres..."
    sleep 1
done

echo Running migrations
python manage.py migrate
# cd /src && python manage.py collectstatic --noinput  # Collect static files

if [ -z "$RUNSERVER" ]
then
    echo Starting using uwsg
    uwsgi --ini uwsgi.ini
else
    echo Starting using manage.py runserver
    python manage.py runserver 0.0.0.0:8080
fi

