import os
import sys
from celery import Celery, shared_task

sys.path.append(os.path.abspath('krm'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")


app = Celery('krm')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
