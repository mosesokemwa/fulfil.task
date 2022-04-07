from celery import Celery
from config import Config


def make_celery(app):
    celery = Celery(
        'tasks',
        backend=Config.CELERY_RESULT_BACKEND,
        broker=Config.CELERY_BROKER_URL,
    )

    # celery.conf.update(Config.CELERY_BROKER_URL)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
