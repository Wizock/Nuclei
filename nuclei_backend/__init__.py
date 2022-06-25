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
from nuclei_backend.extension_globals.database import db


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
            self.import_cors()
            self.import_guard()
            self.import_cookies()
            self.import_blueprints()

    def import_redis(self) -> None:
        """Import the redis."""
        from nuclei_backend.extension_globals.redis import redis_client

        redis_client.init_app(self)

    def return_app(self) -> Flask:
        """Return the app."""
        return self

    def import_config(self) -> None:
        """Import the config."""
        return self.config.from_object("nuclei_backend.config.Config")

    def import_celery(self) -> None:
        """Import the celery."""
        from nuclei_backend.extension_globals.celery import celery

        self.celery = celery

    def import_guard(self) -> None:
        """Import the guard."""
        from nuclei_backend.authentication.models import User
        from nuclei_backend.extension_globals.praetorian import guard

        guard.init_app(self, User)

    def import_db(self) -> None:
        """Import the database."""
        db.init_app(self)
        from nuclei_backend.authentication.models import User
        from nuclei_backend.compression_service.models import media_index
        from nuclei_backend.storage_sequencer.model import FileTracker
        from nuclei_backend.video_compression.models import video_media

        db.create_all()

    def import_security(self) -> None:
        """Import the security."""
        from nuclei_backend.extension_globals.security import security

        security.init_app(self)

    def import_cors(self) -> None:
        """Import the cors."""
        from nuclei_backend.extension_globals.cors import cors

        cors.init_app(
            self,
            resources={
                r"/*": {
                    "origins": "*",
                    "methods": ["OPTIONS", "GET", "POST"],
                    "allow_headers": ["Authorisation"],
                }
            },
        )

    def import_admin(self) -> None:
        """Import the admin."""
        from nuclei_backend.admin_interface.views import \
            admin_interface_blueprint
        from nuclei_backend.extension_globals.admin import admin_instance

        admin_instance.init_app(self)

    def import_cookies(self) -> None:
        """Import the cookies."""
        from nuclei_backend.extension_globals.cookies import login_manager

        login_manager.init_app(self)
        from nuclei_backend.authentication.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

    def import_blueprints(self) -> None:
        """Import the blueprints."""
        from nuclei_backend.authentication.views import auth
        from nuclei_backend.compression_service.views import \
            compression_service_blueprint
        from nuclei_backend.index_mvc.index_view import _index_view
        from nuclei_backend.storage_sequencer.main import \
            storage_sequencer_controller
        from nuclei_backend.video_compression.views import \
            video_compression_blueprint

        self.register_blueprint(compression_service_blueprint)
        self.register_blueprint(video_compression_blueprint)
        self.register_blueprint(auth)
        self.register_blueprint(storage_sequencer_controller)
        self.register_blueprint(_index_view)


# create app instance
app = Nuclei(__name__)
