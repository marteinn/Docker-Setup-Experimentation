#!/bin/bash
# Inspiration from http://michal.karzynski.pl/blog/2015/04/19/packaging-django-applications-as-docker-container-images/

python manage.py migrate                  # Apply database migrations
# cd /src && python manage.py collectstatic --noinput  # Collect static files

echo Starting uwsg
exec uwsgi --ini /uwsgi.ini

