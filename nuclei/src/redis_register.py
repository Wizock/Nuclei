from flask_redis import FlaskRedis
from redis import Redis

from nuclei import Nuclei

# https://realpython.com/flask-by-example-implementing-a-redis-task-queue/


class redis_register(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.redis = FlaskRedis(app)
        self.redis_key = "nuclei_redis_key"

    def register_redis(self):
        self.redis.init_app(self.app)
