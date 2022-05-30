import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    API_PREFIX = "/api"
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True
    CELERY_BROKER_URL = "redis://localhost:6379"
    # CELERY_RESULT_BACKEND = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://"
    UPLOAD_FOLDER = os.path.join(basedir, "uploads")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.environ.get("FLASK_ENV") or "development"
    DEBUG = os.environ.get("DEBUG") or False


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.environ.get("FLASK_ENV") or "production"
    DEBUG = os.environ.get("DEBUG") or False
