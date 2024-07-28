from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

session_factory = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass