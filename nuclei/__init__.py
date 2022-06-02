# import dependances for the nuclei package
import importlib
import os
import secrets

import pytest

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

from nuclei.authentication.tokens import *

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
            self.import_celery()
            self.import_redis()
            self.import_admin()
            self.import_cookies()
            self.import_blueprints()

    def import_redis(self) -> None:
        """Import the redis."""
        from nuclei.extension_globals.redis import redis_client

        redis_client.init_app(self)

    def return_app(self) -> Flask:
        """Return the app."""
        return self

    def import_config(self) -> None:
        """Import the config."""
        return self.config.from_object("nuclei.config.Config")

    def import_celery(self) -> None:
        """Import the celery."""
        from nuclei.extension_globals.celery import celery

        self.celery = celery

    def import_db(self) -> None:
        """Import the database."""
        db.init_app(self)
        from nuclei.authentication.models import User
        from nuclei.compression_service.models import media_index
        from nuclei.video_compression.models import video_media

        db.create_all()

    def import_security(self) -> None:
        """Import the security."""
        from nuclei.extension_globals.security import security

        security.init_app(self)

    def import_admin(self) -> None:
        """Import the admin."""
        from nuclei.admin_interface.views import admin_interface_blueprint
        from nuclei.extension_globals.admin import admin_instance

        admin_instance.init_app(self)

    def import_cookies(self) -> None:
        """Import the cookies."""
        from nuclei.extension_globals.cookies import login_manager

        login_manager.init_app(self)
        from nuclei.authentication.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    def import_tokens(self) -> None:
        """Import the tokens."""
        pass

    def import_blueprints(self) -> None:
        """Import the blueprints."""
        from nuclei.authentication.views import authentication_blueprint
        from nuclei.compression_service.views import compression_service_blueprint
        from nuclei.index_mvc.index_view import _index_view
        from nuclei.video_compression.views import video_compression_blueprint

        self.register_blueprint(compression_service_blueprint)
        self.register_blueprint(video_compression_blueprint)
        self.register_blueprint(authentication_blueprint)
        self.register_blueprint(_index_view)


# create app instance
app = Nuclei(__name__)

from supertokens_python import get_all_cors_headers
from flask_cors import CORS
from supertokens_python.framework.flask import Middleware

Middleware(app)

# TODO: Add APIs

CORS(
    app=app,
    origins=["http://localhost:3000"],
    supports_credentials=True,
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)
