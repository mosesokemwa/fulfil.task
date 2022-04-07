import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    DEBUG = os.environ.get('DEBUG') or False
    CELERY_BROKER_URL="redis://localhost:6379"
    CELERY_RESULT_BACKEND="redis://localhost:6379"
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')


class DevConfig(Config):
   FLASK_ENV = 'development'
   DEBUG = True