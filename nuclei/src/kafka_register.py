from nuclei import Nuclei
from threading import Event
from kafka import KafkaConsumer, KafkaProducer

import signal


class kafka_register(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.TOPIC_NAME = "INFERENCE"
        self.KAFKA_SERVER = "localhost:9092"
        self.
    def register_kafka(self):


