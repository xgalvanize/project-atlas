import os
from celery import Celery

# Tell Celery where the Django settings are
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atlas.settings")

app = Celery("atlas")

# Use Django settings, with CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in apps
app.autodiscover_tasks()
