import os
from celery import app as celery_app


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = celery_app.Celery('task_manager')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()