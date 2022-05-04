# import dependances for the nuclei package
import importlib
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

# create app class
class Nuclei(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super().__init__(import_name, template_folder, root_path)

    def return_app(self) -> Flask:
        return self


from nuclei.blueprint_register import Blueprints_Register
from nuclei.config_register import Config_Register
from nuclei.database_register import Database_Register
from nuclei.extension_register import extensions
from nuclei.security_register import Security_Register
from nuclei.socket_register import Socket_Register
from nuclei.redis_register import Redis_Register
from nuclei.celery_register import Celery_Register
from nuclei.kafka_register import Kafka_Register




class Libraries(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.blueprint_register = Blueprints_Register(self.app)
        self.config_register = Config_Register(self.app)
        self.extension_register = Extension_Register(self.app)
        self.database_register = Database_Register(self.app)



__app__ = Nuclei(__name__)
__libraries__ = Libraries(__app__)


with __app__.app_context():
    __libraries__.blueprint_register.register_blueprints()
    __libraries__.config_register.register_config()
    __libraries__.extension_register.register_extensions()
    __libraries__.database_register.import_tables(__app__)
    __libraries__.database_register.register_extensions()
