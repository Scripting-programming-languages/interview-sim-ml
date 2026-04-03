from kafka import KafkaProducer
import json
import os

producer = KafkaProducer(
    # bootstrap_servers="localhost:9092",
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_to_kafka(topic: str, message: dict):
    producer.send(topic, message)
    producer.flush()