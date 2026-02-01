#!/bin/bash
set -e

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn atlas.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
