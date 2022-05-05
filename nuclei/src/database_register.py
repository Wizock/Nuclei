from flask_sqlalchemy import SQLAlchemy


class Database_Register(object):
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(app)
        
    def return_db(self) :
        return self.db

    def import_tables(self):
        self.db.init_app(self)
        from nuclei.compression_service.models import CompressionService

        # from nuclei.authentication.models import User
        # from nuclei.admin_interface.models import AdminInterface

        self.app.db.create_all()
