from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from nuclei import Nuclei

# export DATABASE_URL="postgresql:///wordcount_dev"


class migrate_register(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.migrate = Migrate(app, app.db)
        self.manager = Manager(app)

    def register_migrate(self):
        self.migrate.init_app(self.app)
        self.manager.add_command("db", MigrateCommand)
        self.manager.add_command("runserver", self.app.runserver)
        self.manager.add_command("shell", self.app.shell)
