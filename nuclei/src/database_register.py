from nuclei import Nuclei


class Database_Register(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.app.config["SQLALCHEMY_ECHO"] = False
        self.app.config["SQLALCHEMY_RECORD_QUERIES"] = False
        self.app.config["SQLALCHEMY_BIND_DECLARED_SOURCES"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/nuclei.db"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    def import_tables(app):
        from nuclei.compression_service.models import CompressionService

        # from nuclei.authentication.models import User
        # from nuclei.admin_interface.models import AdminInterface

        app.db.create_all()
