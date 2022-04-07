from app import create_app

app = create_app()
app.app_context().push()

from tasks import celery


# from celery import Celery
# from config import config

# def make_celery(app):
#     celery = Celery(
#         # backend=Config.CELERY_RESULT_BACKEND,
#         # broker=Config.CELERY_BROKER_URL,
#         __name__,
#         backend=config.CELERY_RESULT_BACKEND,
#         broker=config.CELERY_BROKER_URL,
#     )

#     celery.conf.update(config.as_dict())
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery
