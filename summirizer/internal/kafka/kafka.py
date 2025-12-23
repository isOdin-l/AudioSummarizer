import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from configs.config import kafkaConfig
from internal.s3.s3 import s3_client
from internal.database.queries import craete_summary
from internal.database.postgres import get_db
from internal.summirizer_llm import SummirizerLLM
import io 
import uuid

class KafkaWorker():
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            kafkaConfig.KAFKA_TOPIC_CONSUME,
            bootstrap_servers=kafkaConfig.KAFKA_BOOTSTRAP_SERVERS,
            group_id=kafkaConfig.KAFKA_GROUP_ID,
            enable_auto_commit=False,
            session_timeout_ms=30000,      
            heartbeat_interval_ms=10000,     
            max_poll_interval_ms=300000  
        )

        self.producer = AIOKafkaProducer(
            bootstrap_servers=kafkaConfig.KAFKA_BOOTSTRAP_SERVERS
        )

    async def send(self, message: dict):
        if not self.producer:
            raise RuntimeError("Kafka producer is not started")
        
        await self.producer.send_and_wait(kafkaConfig.KAFKA_TOPIC_PRODUCE, value=json.dumps(message).encode("utf-8"))


    async def kafka_processor(self):
        try:
            async for msg in self.consumer:
                data = json.loads(msg.value)
                
                audio_data = await s3_client.download_file(object_name = data["s3_filename"])
                audio_text = audio_data.decode("utf-8")
                
                
                result_text = await SummirizerLLM.summirize(audio_text)
                
                summary_name = uuid.uuid4()
                with get_db() as db:
                    await craete_summary(db = db, audio_id= data["audio_id"], filename = summary_name)
                
                # Преобразование текста в байты, затем в поток binaryio, затем добавление в s3
                binary_text = result_text.encode("utf-8")
                text_file = io.BytesIO(binary_text)
                text_file.seek(0)
                await s3_client.upload_file(file_data = text_file, object_name = summary_name, file_length = len(binary_text), content_type="txt/plain")

                # Отправка в целевой топик 
                await self.send({"s3_filename": str(summary_name), "interaction_data": data["interaction_data"], "audio_id": data["audio_id"]})
                # Явное подтверждение оффсета
                await self.consumer.commit()
                print("OK")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            await self.consumer.stop()
            await self.producer.stop()