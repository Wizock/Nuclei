# import dependances for the nuclei package
import importlib
import os
import secrets

# import flask_security
from flask import Flask
from flask_admin import Admin
from flask_caching import Cache
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
# from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from nuclei.extension_globals.database import db


# create app class
class Nuclei(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super().__init__(import_name, template_folder, root_path)
        with self.app_context():

            self.import_config()
            self.import_db()
            self.import_blueprints()

    def return_app(self) -> Flask:
        return self

    def import_config(self) -> None:
        return self.config.from_object("nuclei.config.Config")

    def import_db(self) -> None:
        db.init_app(self)
        from nuclei.authentication.models import User_Auth
        from nuclei.compression_service.models import media_index, compression_index

        db.create_all()

    def import_blueprints(self) -> None:
        from nuclei.compression_service.views import \
            compression_service_blueprint

        self.register_blueprint(compression_service_blueprint)


# create app instance
app = Nuclei(__name__)
