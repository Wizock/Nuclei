from nuclei import Nuclei


class Database_Register(object):
    def __init__(self, app: Nuclei):
        self.app = app

    def import_tables(app):
        from nuclei.compression_service.models import CompressionService

        # from nuclei.authentication.models import User
        # from nuclei.admin_interface.models import AdminInterface

        app.db.create_all()
