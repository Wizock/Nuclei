from nuclei import Nuclei
import secrets


class Config_Register(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.app.config["SECRET_KEY"] = secrets.token_hex(16)

        self.app.config["DEBUG"] = True
        self.app.config["CACHE_TYPE"] = "simple"
        self.app.config["CACHE_DEFAULT_TIMEOUT"] = 300

        self.app.config["MAIL_SERVER"] = "smtp.gmail.com"
        self.app.config["MAIL_PORT"] = 465
        self.app.config["MAIL_USE_SSL"] = True
