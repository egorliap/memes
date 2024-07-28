import os
import asyncio
from typing import BinaryIO

from dotenv import load_dotenv
from miniopy_async import Minio

load_dotenv()


class MinioClient:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.client = Minio(
            access_key=access_key,
            secret_key=secret_key,
            endpoint=endpoint_url,
            secure=False
        )
        self.bucket_name = bucket_name


    async def init_bucket(self):
        if(not await self.client.bucket_exists(self.bucket_name)):
            await self.client.make_bucket(self.bucket_name)
        
        
    async def upload_file(self, object_name: str, file: BinaryIO, file_size: int):
        await self.client.put_object(self.bucket_name,
                               object_name=object_name,
                               data=file,
                               length=file_size,
                                )
        
        
    async def get_file_url(self, object_name: str):
        return await self.client.get_presigned_url(method="GET",
                                      bucket_name=self.bucket_name,
                                      object_name=object_name)
        
        
    async def delete_file(self, object_name: str):
        await self.client.remove_object(bucket_name=self.bucket_name,
                                  object_name=object_name)


s3_client = MinioClient(
        access_key=os.getenv("MINIO_ROOT_USER"),
        secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
        endpoint_url=os.getenv("MINIO_ENDPOINT_HOST")+":"+os.getenv("MINIO_ENDPOINT_PORT"),
        bucket_name="bucket",
    )



