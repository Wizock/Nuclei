import os
from datetime import timedelta

from celery import Celery
from flask_cors import CORS


class Config(object):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_BIND_DECLARED_SOURCES = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/nuclei.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(
        os.getcwd(), "nuclei", "compression_service", "file_storage"
    )
    FLASK_ADMIN_SWATCH = "cyborg"
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    REDIS_URL = "redis://:password@localhost:6379"
    MAX_CONTENT_LENGTH = 2450 * 1024 * 1024

    CORS_HEADERS = "Content-Type"
    SESSION_COOKIE_NAME = "google-login-session"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    JWT_ACCESS_LIFESPAN = {"hours": 24}
    JWT_REFRESH_LIFESPAN = {"days": 30}


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Development configuration"""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
