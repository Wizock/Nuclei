# import dependances for the nuclei package
import secrets
from secrets import token_urlsafe

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
        self.config["SECRET_KEY"] = secrets.token_hex(16)
        self.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/nuclei.db"
        self.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.config["SQLALCHEMY_ECHO"] = False
        self.config["MAIL_SERVER"] = "smtp.gmail.com"
        self.config["MAIL_PORT"] = 465
        self.config["MAIL_USE_SSL"] = True

        self.db = SQLAlchemy(self)
        self.migrate = Migrate(self, self.db)
        # self.login_manager = LoginManager(self)
        # self.login_manager.login_view = "auth.login"
        self.mail = Mail(self)
        self.admin = Admin(self, name="Nuclei")
        self.cors = CORS(self, resources={r"/*": {"origins": "*"}})
        self.socketio = SocketIO(self)
        self.cache = Cache(self)
        self.debugtoolbar = DebugToolbarExtension(self)

        self.register_extensions()

    def return_db(self) -> SQLAlchemy:
        return self.db

    def register_blueprints(self):
        from nuclei.admin_interface.views import admin_interface_blueprint
        from nuclei.authentication.views import authentication_blueprint
        from nuclei.compression_service.views import compression_service_blueprint

        self.register_blueprint(compression_service_blueprint)
        self.register_blueprint(admin_interface_blueprint)
        self.register_blueprint(authentication_blueprint)

    def register_extensions(self):
        self.db.init_app(self)
        self.migrate.init_app(self)
        # self.login_manager.init_app(self)
        self.mail.init_app(self)
        self.cors.init_app(self)
        self.socketio.init_app(self)
        self.cache.init_app(self)
        self.debugtoolbar.init_app(self)


app = Nuclei(__name__)

with app.app_context():
    import_tables(app)
    app.register_blueprints()
