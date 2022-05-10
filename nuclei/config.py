import os


class Config(object):
    DEBUG = False
    TESTING = False
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
    ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    FLASK_ADMIN_SWATCH = 'cyborg' 


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
