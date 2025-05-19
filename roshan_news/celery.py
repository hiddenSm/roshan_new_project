import os

from twisted.internet import asyncioreactor
try:
    asyncioreactor.install()
except Exception as e:
    # print(e)
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roshan_news.settings')

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roshan_news.settings')

app = Celery('roshan_news')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
