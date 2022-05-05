from flask_sqlalchemy import SQLAlchemy


class database_object(object):
    def __init__(self, app):
        self.app = app
        self.db = SQLAlchemy(app)

    def return_db(self) -> SQLAlchemy:
        return self.db

    def register_models(self):
        from nuclei.compression_service.models import CompressionService

        self.db.create_all()
        self.db.session.commit()
