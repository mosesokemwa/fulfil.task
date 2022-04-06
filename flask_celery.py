from celery import Celery
from config import Config


def make_celery(app):
    celery = Celery(
        app,
        backend=Config.CELERY_RESULT_BACKEND,
        broker=Config.CELERY_BROKER_URL,
    )

    celery.conf.update(
        CELERY_TASK_SERIALIZER="json",
        CELERY_RESULT_SERIALIZER="json",
        CELERY_ACCEPT_CONTENT=["json"],
        CELERY_TIMEZONE="Europe/Oslo",
        CELERY_ENABLE_UTC=True,
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
