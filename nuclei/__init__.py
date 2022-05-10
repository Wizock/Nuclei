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
    """
    Nuclei class.
    """

    def __init__(
        self, import_name: str, template_folder: None = None, root_path: None = None
    ) -> None:
        """
        Initialize the app.
        :param import_name: app's import name
        :param template_folder: app's template folder
        :param root_path: app's root path

        """
        super().__init__(import_name, template_folder, root_path)
        with self.app_context():

            self.import_config()
            self.import_db()
            self.import_blueprints()
            self.import_admin()
            self.import_cookies()

    def return_app(self) -> Flask:
        """
        Return the app.
        """
        return self

    def import_config(self) -> None:
        """
        Import the config.
        """
        return self.config.from_object("nuclei.config.Config")

    def import_db(self) -> None:
        """
        Import the database.
        """
        db.init_app(self)
        from nuclei.authentication.models import User
        from nuclei.compression_service.models import media_index

        db.create_all()

    def import_admin(self) -> None:
        """
        Import the admin.
        """
        from nuclei.extension_globals.admin import admin_instance

        admin_instance.init_app(self)

    def import_cookies(self) -> None:
        """
        Import the cookies.
        """
        from nuclei.extension_globals.cookies import login_manager

        login_manager.init_app(self)
        from nuclei.authentication.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    def import_blueprints(self) -> None:
        """
        Import the blueprints.
        """
        from nuclei.authentication.views import authentication_blueprint
        from nuclei.compression_service.views import compression_service_blueprint

        self.register_blueprint(compression_service_blueprint)
        self.register_blueprint(authentication_blueprint)


# create app instance
app = Nuclei(__name__)
