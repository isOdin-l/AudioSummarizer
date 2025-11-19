from aiokafka import AIOKafkaProducer
from core.settings.settings import kafkaConfig
import json


class KafkaClient:
    def __init__(self):
        pass
    async def start_producer(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=kafkaConfig.KAFKA_BOOTSTRAP_SERVERS)
        await self.producer.start()

    async def stop_producer(self):
        if self.producer:
            await self.producer.stop()

    async def send(self, message: dict):
        if not self.producer:
            raise RuntimeError("Kafka producer is not started")
        
        await self.producer.send_and_wait(kafkaConfig.KAFKA_TOPIC, value=json.dumps(message).encode("utf-8"))

kafka_client = KafkaClient()