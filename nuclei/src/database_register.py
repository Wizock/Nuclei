from flask_sqlalchemy import SQLAlchemy


class Database_Register(object):
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(app)
        self.config["SQLALCHEMY_ECHO"] = False
        self.config["SQLALCHEMY_RECORD_QUERIES"] = False
        self.config["SQLALCHEMY_BIND_DECLARED_SOURCES"] = True
        self.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/nuclei.db"
        self.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    def return_db(self) -> SQLAlchemy:
        return self.db

    def import_tables(self, app):
        self.db.init_app(self)
        from nuclei.compression_service.models import CompressionService

        # from nuclei.authentication.models import User
        # from nuclei.admin_interface.models import AdminInterface

        app.db.create_all()
