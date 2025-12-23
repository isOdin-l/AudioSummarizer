from minio import Minio
from minio.error import S3Error
from configs.config import s3Config

class S3Client:
    def __init__(self):
        self.client = Minio(
            s3Config.S3_ENDPOINT,
            access_key=s3Config.S3_ACCESS_KEY,
            secret_key=s3Config.S3_SECRET_KEY,
            region=s3Config.S3_REGION,
            secure=False
        )

    async def download_file(self, object_name: str):
        try:
            response = self.client.get_object(
                bucket_name = s3Config.S3_BUCKET, 
                object_name = object_name
            )
            
            file_data = response.read()
            
            return file_data
        except S3Error as e:
            raise RuntimeError(f"Ошибка скачивания из S3: {e}")
        finally:
            response.close()
            response.release_conn()

s3_client = S3Client()