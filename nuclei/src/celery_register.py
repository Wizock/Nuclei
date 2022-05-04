import celery
from celery import Celery

from nuclei import Nuclei

# https://flask.palletsprojects.com/en/2.1.x/patterns/celery/


class Celery_Register(object):
    def __init__(self, app: Nuclei):
        self.celery = Celery(
            app.import_name,
            broker=app.config["CELERY_BROKER_URL"],
            backend=app.config["CELERY_RESULT_BACKEND"],
        )
        self.app = app
        self.celery.conf.update(app.config)
        self.celery.conf.update(app.config["CELERY_TASK_DEFAULT_QUEUE"])
        self.celery.conf.update(app.config["CELERY_TASK_DEFAULT_EXCHANGE"])
        self.celery.conf.update(app.config["CELERY_TASK_DEFAULT_ROUTING_KEY"])
        self.celery.conf.update(app.config["CELERY_TASK_DEFAULT_EXCHANGE_TYPE"])
        self.celery.conf.update(app.config["CELERY_TASK_DEFAULT_DELIVERY_MODE"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with self.app.app_context():
                return self.run(*args, **kwargs)

    def task_register(self) -> Celery:
        celery.Task = self.ContextTask
        return self.celery
    