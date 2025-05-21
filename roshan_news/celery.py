import os, sys


if 'flower' not in sys.argv:
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

from celery.schedules import crontab

app.conf.beat_schedule = {
    'scrap_news': {
        'task': 'news.tasks.crawl_zoomit',
        'schedule': crontab(minute='*/1'),
    },
}