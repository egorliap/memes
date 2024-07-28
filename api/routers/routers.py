import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,Response, UploadFile
import json
from fastapi.responses import FileResponse, StreamingResponse

from api.schemas import MemeCreate, MemeCreateOrm, MemeDB
from api.db import MemeOrm
from media_service import s3_client


IMAGE_EXTENSIONS = {"jpg","png"}

router = APIRouter(
    prefix="/memes",
    tags=["Memes!"]
)


@router.get("/{id}")
async def get_meme(id: int):
    meme = await MemeOrm.get_meme_by_id(id)
    if(meme):
        meme.url = await s3_client.get_file_url(meme.name)
        return Response(status_code=200,
                        content=json.dumps({"success":"true",
                                 "message":f"Meme with id of {id} is found",
                                 "meme":meme.model_dump()}),
                        media_type="application/json")
    else:
        return Response(status_code=404,
                        content=json.dumps({"success":"false",
                                            "message":"Meme not found"}),
                        media_type="application/json")


@router.get("/")
async def get_memes(size: int=20,page: int=1):
    memes = await MemeOrm.get_memes(limit=size,offset=page)
    content = []
    for meme in memes:
        meme.url = await s3_client.get_file_url(meme.name)
        content.append(meme.model_dump())
    return Response(status_code=200,
                    content=json.dumps({"success":"true",
                                        "message":"Memes found",
                                        "page":page,
                                        "size":size,
                                        "memes":content}),
                    media_type="application/json")


@router.post("/")
async def add_meme(meme: Annotated[MemeCreate,Depends()]):
    ext = meme.file.filename.split(".")[-1]
    if(ext not in IMAGE_EXTENSIONS):
        return Response(status_code=400,
                        content=json.dumps(
                            {"success":"false",
                             "message":"Extension of the file is not supported"}
                            ),
                        media_type="application/json")
    
    filename = str(uuid.uuid4()) + "." + ext
    
    
    await s3_client.upload_file(filename,meme.file.file,meme.file.size)
    new_meme_id = await MemeOrm.add_meme(MemeCreateOrm(name=filename,description=meme.description))
        
    return Response(status_code=200,
                    content=json.dumps(
                            {"success":"true",
                            "message":f"New meme is added with id of {new_meme_id}"}
                            ),
                    media_type="application/json")

        

@router.put("/{id}")
async def update_meme(id: int, meme: Annotated[MemeCreate,Depends()]):
    meme_update = await MemeOrm.get_meme_by_id(id)
    s3_client.delete_file(meme_update.name)
    
    # to outer handler 
    ext = meme.file.filename.split(".")[-1]
    if(ext not in IMAGE_EXTENSIONS):
        return Response(status_code=400,
                        content=json.dumps(
                            {"success":"false",
                             "message":"Extension of the file is not supported"}
                            ),
                        media_type="application/json")
    
    filename = str(uuid.uuid4()) + "." + ext
    updated = MemeCreateOrm(description=meme.description,name=filename)
    
    await MemeOrm.update_meme(id,updated)
    
    await s3_client.upload_file(filename,meme.file.file,meme.file.size)
    
    return Response(status_code=200,
                    content=json.dumps(
                            {"success":"true",
                            "message":f"Meme with id of {id} updated"}
                            ),
                    media_type="application/json")

    
@router.delete("/{id}")
async def delete_meme(id: int):
    meme_delete = await MemeOrm.get_meme_by_id(id)
    if(meme_delete):
        await s3_client.delete_file(meme_delete.name)
        await MemeOrm.delete_meme(meme_delete.id)
        return Response(status_code=200,
                        content=json.dumps({"success":"true",
                                "message":f"Meme with id of {meme_delete.id} is deleted"}),
                        media_type="application/json")
    else:
        return Response(status_code=404,
                        content=json.dumps({"success":"false",
                                "message":f"Meme with id of {id} doesn't exist"}),
                        media_type="application/json")
        