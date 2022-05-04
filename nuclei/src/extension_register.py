from nuclei import Nuclei


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
