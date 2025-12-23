import asyncio
from internal.kafka.kafka import KafkaWorker

async def main():
    kafka = KafkaWorker()

    await kafka.consumer.start()
    await kafka.producer.start()

    await kafka.kafka_processor()

asyncio.run(main())