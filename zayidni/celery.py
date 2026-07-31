from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zayidni.settings')

app = Celery('zayidni')
# Read config from Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')
# Autodiscover tasks in installed apps
app.autodiscover_tasks()


if __name__ == '__main__':
    app.start()
