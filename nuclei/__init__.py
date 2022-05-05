# import dependances for the nuclei package
import importlib
import secrets
from secrets import token_urlsafe

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
    
    def import_config(self):
        self.config.from_object("nuclei.config.Config")
        self.config.from_pyfile("config.py")


from nuclei.src.blueprint_register import Blueprints_Register
from nuclei.src.database_register import Database_Register


class Libraries(object):
    def __init__(self, app: Nuclei):

        self.app: Nuclei = app
        self.db_obj = Database_Register(app)
        self.blueprint_register = Blueprints_Register(self.app)

    def return_db(self) -> SQLAlchemy:
        return self.db_obj.return_db()

    def import_tables(self):
        self.db_obj.import_tables()


__app__ = Nuclei(__name__).return_app()
__libraries__ = Libraries(__app__)
with __app__.app_context():
    with __libraries__.return_db().engine.connect() as connection:
        __libraries__.import_tables()
    __libraries__.blueprint_register.register_blueprints()

