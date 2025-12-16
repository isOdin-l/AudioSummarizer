from pydantic_settings import BaseSettings


class Config:
    env_file = None
    extra = "ignore"

class S3Config(BaseSettings, Config):
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_CONSUMER: str
    S3_BUCKET_PRODUCER: str
    S3_REGION: str

class PostgresConfig(BaseSettings, Config):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

class KafkaConfig(BaseSettings, Config):
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_GROUP_ID: str
    KAFKA_TOPIC_CONSUME: str
    KAFKA_TOPIC_PRODUCE: str

kafkaConfig = KafkaConfig()
s3Config = S3Config()
postgresConfig = PostgresConfig()