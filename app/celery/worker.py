from celery import Celery

from ..config import settings


celery = Celery(__name__, broker=settings.CELERY_BROKER_URL, include=settings.CELERY_IMPORTS)
celery.conf.update(dict(CELERY_TIMEZONE=settings.CELERY_TIMEZONE))
