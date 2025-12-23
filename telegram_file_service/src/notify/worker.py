from dotenv import load_dotenv
load_dotenv()

import asyncio, json
from aiokafka import AIOKafkaConsumer
import boto3

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os


KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "summary_topic")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

s3 = boto3.client("s3")

async def main():
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="tg_notify",
        enable_auto_commit=True,
        auto_offset_reset="latest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            payload = json.loads(msg.value.decode("utf-8"))
            chat_id = int(payload["interaction_data"])
            bucket = payload["s3_bucket"]
            key = payload["s3_key"]

            obj = s3.get_object(Bucket=bucket, Key=key)
            summary_text = obj["Body"].read().decode("utf-8")

            await bot.send_message(chat_id, f"Суммаризация готова:\n\n{summary_text}")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(main())
