from nuclei import Nuclei


class Blueprints_Register(object):
    def __init__(self, app: Nuclei):
        self.app = app

    def register_blueprints(self):
        from nuclei.admin_interface.views import admin_interface_blueprint
        from nuclei.authentication.views import authentication_blueprint
        from nuclei.compression_service.views import compression_service_blueprint

        self.app.register_blueprint(compression_service_blueprint)
        self.app.register_blueprint(admin_interface_blueprint)
        self.app.register_blueprint(authentication_blueprint)
