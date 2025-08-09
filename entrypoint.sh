#!/bin/sh

set -e

echo "Applying database migrations..."
python poll_project/manage.py migrate --noinput

echo "Collecting static files..."
python poll_project/manage.py collectstatic --noinput

echo "Starting Django server..."
gunicorn poll_project.wsgi:application --chdir poll_project --bind 0.0.0.0:$PORT