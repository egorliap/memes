import asyncio
import os

import aiohttp
from dotenv import load_dotenv
from fastapi import UploadFile
import asyncio_atexit

load_dotenv()

MEDIA_HOST = os.getenv("MEDIA_HOST")
MEDIA_PORT = os.getenv("MEDIA_PORT")
MEDIA_ACCESS_KEY = os.getenv("MEDIA_ACCESS_KEY")

media_url = "http://" + MEDIA_HOST + ":" + MEDIA_PORT + "/"

session = aiohttp.ClientSession()


async def add_media(media: UploadFile):
    async with session.post(media_url,data={"file":media.file.read()}) as res:
        if res.status == 200:
            return True
    return False


async def get_media(media_name: str):
    async with session.get(media_url+f"{media_name}") as res:
        if res.status == 200:
            return await res.text()
    return None


async def delete_media(media_name: str):
    async with session.delete(media_url+f"{media_name}") as res:
        if res.status == 200:
            return True
    return False

asyncio_atexit.register(session.close())