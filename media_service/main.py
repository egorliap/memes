from typing import BinaryIO
from fastapi import FastAPI, File, Response, UploadFile

from .client import s3_client

app = FastAPI()


@app.post("/")
async def add_media(file: UploadFile):
    try:
        await s3_client.upload_file(file.filename,file.file,file.size)
        return Response(status_code=200)
    except:
        Response(status_code=400)
        
        
@app.get("/{filename}")
async def get_media(filename: str):
    try:
        res = await s3_client.get_file_url(filename)
        return Response(status_code=200,
                        content=res,
                        media_type="text/plain;charset=UTF-8")
    except:
        Response(status_code=400)
        

@app.delete("/{filename}")
async def delete_media(filename: str):
    try:
        await s3_client.delete_file(filename)
        return Response(status_code=200)
    except:
        Response(status_code=400)