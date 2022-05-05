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



# create app class
class Nuclei(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super().__init__(import_name, template_folder, root_path)

    def return_app(self) -> Flask:
        return self

    def import_config(self) -> None:
        return self.config.from_object("nuclei.config.Config")


class NucleiApp(Nuclei):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super().__init__(import_name, template_folder, root_path)

    @staticmethod
    def extension_init(self) -> None:

        # create database instance
        __db__ = database_object(__app__)

        # create cache instance
        __cache__ = Cache(__app__)
        # create admin instance
        __admin__ = Admin(__app__, name="Nuclei", template_mode="bootstrap3")
        # create migrate instance
        __migrate__ = Migrate(__app__, __db__)
        # create socketio instance
        __socketio__ = SocketIO(__app__)
        # create mail instance
        __mail__ = Mail(__app__)
        # create debugtoolbar instance
        __debugtoolbar__ = DebugToolbarExtension(__app__)
        # create cors instance
        __cors__ = CORS(__app__)
        # create login instance

from nuclei.src.database_register import database_object

# create app instance
__app__ = Nuclei(__name__)
with __app__.app_context():
    __app__.import_config()
    __deps__ = NucleiApp(__name__)
    __deps__.extension_init(__app__)
