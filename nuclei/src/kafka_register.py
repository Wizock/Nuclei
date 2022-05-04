from nuclei import Nuclei
from kafka import KafkaConsumer, KafkaProducer
import os, json, uuid
from concurrent.futures import ThreadPoolExecutor


class kafka_register(object):
    def __init__(self, app: Nuclei):
        self.app = app
        self.TOPIC_NAME = "INFERENCE"
        self.KAFKA_SERVER = "localhost:9092"
        self.NOTIFICATION_TOPIC = "NOTIFICATION"
        self.EMAIL_TOPIC = "EMAIL"

    def register_kafka(self):
        
        self.consumer = KafkaConsumer(
            self.TOPIC_NAME,
            bootstrap_servers=self.KAFKA_SERVER,
            # to deserialize kafka.producer.object into dict
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        self.producer = KafkaProducer(
            bootstrap_servers=self.KAFKA_SERVER,
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )
        self.notification_consumer = KafkaConsumer(
            self.NOTIFICATION_TOPIC,
            bootstrap_servers=self.KAFKA_SERVER,
            # to deserialize kafka.producer.object into dict
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        self.email_consumer = KafkaConsumer(
            self.EMAIL_TOPIC,
            bootstrap_servers=self.KAFKA_SERVER,
            # to deserialize kafka.producer.object into dict
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
    
    def infrence_process_function(self, data):
        """
        . . . . .

        . . . . .
        . . . . .
        process steps
        . . . . .
        . . . . .
        """

        self.producer.send(self.NOTIFICATION_TOPIC, data)
        self.producer.flush()
        self.producer.send(self.EMAIL_TOPIC, data)
        self.producer.flush()
