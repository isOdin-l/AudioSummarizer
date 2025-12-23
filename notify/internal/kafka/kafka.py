import json
from aiokafka import AIOKafkaConsumer
from internal.s3.s3 import s3_client
from configs.config import kafkaConfig
import requests

class KafkaWorker():
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            kafkaConfig.KAFKA_TOPIC,
            bootstrap_servers=kafkaConfig.KAFKA_BOOTSTRAP_SERVERS,
            group_id=kafkaConfig.KAFKA_GROUP_ID,
            enable_auto_commit=False,
            session_timeout_ms=30000,      
            heartbeat_interval_ms=10000,     
            max_poll_interval_ms=300000  
        )

    async def kafka_processor(self):
        try:
            async for msg in self.consumer:
                data = json.loads(msg.value)
                
                sum_data = await s3_client.download_file(object_name = data["s3_filename"])
                sum_text = sum_data.decode("utf-8")

                print(sum_text)

                # requests.post("http://tg-bot-service:8081/send-notification", json=json.dumps(data)) # тут отправляем реквест на сервер бота, который потом ответит польвателю
                await self.consumer.commit()
                print("OK")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            await self.consumer.stop()

