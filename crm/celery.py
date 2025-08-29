import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

# Initialize Celery app
app = Celery("crm")

# Configure Celery to use Redis as the broker
app.conf.broker_url = "redis://localhost:6379/0"

# Load task settings from Django settings, with CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks from all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """A simple debug task to verify Celery is working"""
    print(f"Request: {self.request!r}")
