from fastapi import FastAPI
from contextlib import asynccontextmanager

from api import router as meme_router
from api.db import Base, engine, Meme
from media_service import s3_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    await s3_client.init_bucket()

    yield 



app = FastAPI(title="MemeApp",lifespan=lifespan)
app.include_router(meme_router)