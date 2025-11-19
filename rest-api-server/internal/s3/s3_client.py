from minio import Minio
from minio.error import S3Error
from core.settings.settings import s3Config
from typing import BinaryIO
import uuid


class S3Client:
    def __init__(self):

        self.client = Minio(
            s3Config.S3_ENDPOINT,
            access_key=s3Config.S3_ACCESS_KEY,
            secret_key=s3Config.S3_SECRET_KEY,
            region=s3Config.S3_REGION,
            secure=False
        )

    async def upload_file(self, file_data: BinaryIO, file_length: int, object_name: uuid, content_type: str):
        try:
            self.client.put_object(
                bucket_name=s3Config.S3_BUCKET,
                object_name=str(object_name),
                data=file_data,
                length=file_length,
                content_type=content_type,
            )
        except S3Error as e:
            raise RuntimeError(f"Error uploading to S3: {e}")

s3_client = S3Client()