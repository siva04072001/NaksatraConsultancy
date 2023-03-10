from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','helpdesk.settings')

app=Celery('celeryapp')
app.conf.enable_utc=False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')
celery=Celery(__name__)
celery.conf.broker_url="redis://redis:6379/0"
celery.conf.result_backend="redis://redis:6379/0"


#celery beat settings
app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule ={
    'tickets-task1': {
        'task': 'tickets.views.mail_alert',
        'schedule': crontab(hour=16, minute=0)
    },
    'tickets-task2': {
        'task': 'tickets.views.expiry_mail',
        'schedule': crontab(hour=9, minute=0)
    },
}