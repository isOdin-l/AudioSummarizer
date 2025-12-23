import json
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from configs.config import kafkaConfig
from internal.s3.s3 import s3_client
from internal.database.queries import create_transcription
from internal.database.postgres import get_db
from internal.transcriber import transcriber
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
                data = json.loads(msg.value) # Mb обрабатывать ошибку

                # Процесс транскрибации: получение из s3 аудио файла ->  транскрибация -> запись в бд -> запись в s3-> вывод информации о записи
                audio_data = await s3_client.download_file(object_name = data["s3_filename"])
                result_text = await transcriber.transcribe(audio_data)
                
                # создание записи в бд о тексте
                tr_name= uuid.uuid4()
                with get_db() as db:
                    await create_transcription(db = db, audio_id= data["audio_id"], filename = tr_name)
                
                # Преобразование текста в байты, затем в поток binaryio, затем добавление в s3
                binary_text = result_text.encode("utf-8")
                text_file = io.BytesIO(binary_text)
                text_file.seek(0)
                await s3_client.upload_file(file_data = text_file, object_name = tr_name, file_length = len(binary_text), content_type="txt/plain")

                await self.send({"s3_filename": str(tr_name), "interaction_data": data["interaction_data"]})
                
                # Явное подтверждение оффсета
                await self.consumer.commit()
        
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            await self.consumer.stop()
            await self.producer.stop()