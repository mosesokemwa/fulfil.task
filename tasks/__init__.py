from celery import Celery
import config as config


def make_celery():
   celery = Celery('tasks', broker=config.CELERY_BROKER_URL)
   celery.conf.update(config.as_dict())
   return celery


celery = make_celery()