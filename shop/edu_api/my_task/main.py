import os
import django
from celery import Celery

app = Celery("edu")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edu_api.settings.develop')
django.setup()

app.config_from_object("my_task.config")

app.autodiscover_tasks(['my_task.sms'])

