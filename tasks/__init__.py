from celery import Celery
import config


def make_celery():
   celery = Celery('tasks', broker=config.as_dict()[config.CURRENT_ENV].CELERY_BROKER_URL)
   celery.conf.update(config.as_dict())
   return celery


celery = make_celery()