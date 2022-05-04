# import dependances for the nuclei package
import secrets
from secrets import token_urlsafe

import flask_security
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

from nuclei.database import import_tables


# create app class
class Nuclei(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super().__init__(import_name, template_folder, root_path)
        self.db = SQLAlchemy(self)

    def return_db(self) -> SQLAlchemy:
        return self.db




class Database_Register(object):
    def __init__(self, app: Nuclei):
        self.app = app

    def register_database(self):
        import_tables(self.app)

class Config_Register(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.app.config["SECRET_KEY"] = secrets.token_hex(16)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/nuclei.db"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.config["DEBUG"] = True
        self.app.config["CACHE_TYPE"] = "simple"
        self.app.config["CACHE_DEFAULT_TIMEOUT"] = 300
        self.app.config["SQLALCHEMY_ECHO"] = False
        self.app.config["SQLALCHEMY_RECORD_QUERIES"] = False
        self.app.config["SQLALCHEMY_BIND_DECLARED_SOURCES"] = True
        self.app.config["MAIL_SERVER"] = "smtp.gmail.com"
        self.app.config["MAIL_PORT"] = 465
        self.app.config["MAIL_USE_SSL"] = True


class extensions(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.migrate = Migrate(self, self.db)
        self.mail = Mail(self)
        self.admin = Admin(self, name="Nuclei")
        self.cors = CORS(self, resources={r"/*": {"origins": "*"}})
        self.socketio = SocketIO(self)
        self.cache = Cache(self)
        self.debugtoolbar = DebugToolbarExtension(self)

    def register_extensions(self):
        self.db.init_app(self)
        self.migrate.init_app(self)
        self.mail.init_app(self)
        self.cors.init_app(self)
        self.socketio.init_app(self)
        self.cache.init_app(self)
        self.debugtoolbar.init_app(self)


__app__ = Nuclei(__name__)
Configurations = Configs()
extensions = extensions()

with __app__.app_context():
    import_tables(__app__)
    __app__.register_blueprints()
    __app__.config.from_object(Configurations)
    extensions().register_extensions()
