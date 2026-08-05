"""Celery setup: the worker process that runs jobs outside the web request.

A web request should answer in milliseconds. Anything slower -- rematching
the whole bench, recomputing forecasts -- goes on a queue and a separate
worker process picks it up.
"""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("benchflow")

# Read CELERY_* keys straight out of Django settings.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Find every tasks.py in the installed apps automatically.
app.autodiscover_tasks()
