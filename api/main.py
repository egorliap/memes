from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers.routers import router as meme_router
from .db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield 


app = FastAPI(title="MemeApp",lifespan=lifespan)
app.include_router(meme_router)