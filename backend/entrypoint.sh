#!/bin/bash
set -e

# Run migrations
python manage.py migrate --noinput

# Create Django superuser if ADMIN_USERNAME and ADMIN_PASSWORD are provided
if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_PASSWORD" ]; then
	echo "Checking/creating superuser $ADMIN_USERNAME"
	python - <<'PY'
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atlas.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('ADMIN_USERNAME')
email = os.environ.get('ADMIN_EMAIL', '')
password = os.environ.get('ADMIN_PASSWORD')
if username and password:
		if not User.objects.filter(username=username).exists():
				User.objects.create_superuser(username, email, password)
				print('Created superuser', username)
		else:
				print('Superuser exists', username)
PY
else
	echo "ADMIN_USERNAME or ADMIN_PASSWORD not set; skipping superuser creation"
fi

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn atlas.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
