import os

from celery import Celery

from .base import MarketCelery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

celery_app = Celery('market', task_cls=MarketCelery)

celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.task_default_priority = 5
celery_app.conf.task_default_queue = 'market'
celery_app.conf.task_default_exchange = 'market_exchange'
celery_app.conf.task_default_routing_key = 'market_routing_key'
celery_app.autodiscover_tasks()

