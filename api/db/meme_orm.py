from typing import List
from sqlalchemy import delete, select, update

from .meme_model import Meme
from .base import session_factory
from api.schemas import MemeCreateOrm, MemeDB


class MemeOrm:
    @classmethod
    async def get_meme_by_id(cls, id:int)-> MemeDB|None:
        async with session_factory() as session:
            q = select(Meme).filter(
                Meme.id == id
            )
            res = await session.execute(q)
            scalar = res.scalars().one_or_none()
            if(scalar):
                return MemeDB.model_validate(scalar)
            else:
                return None
    
    
    @classmethod
    async def get_memes(cls, limit: int=20, offset: int=1)-> List[MemeDB|None]:
        async with session_factory() as session:
            q = select(Meme).limit(limit).offset(limit*(offset-1))
            res = await session.execute(q)
            return [MemeDB.model_validate(meme) for meme in res.scalars().all()]
    
    
    @classmethod
    async def add_meme(cls, meme:MemeCreateOrm)-> int:
        async with session_factory() as session:  
            new_meme = Meme(**meme.model_dump())         
            session.add(new_meme)
            await session.flush()
            await session.commit()
            await session.refresh(new_meme)
            return new_meme.id
    
    @classmethod
    async def update_meme(cls,id:int,meme:MemeCreateOrm)-> None:
        async with session_factory() as session:
            stmt = update(Meme)\
                .filter(Meme.id == id)\
                .values(name=meme.name,description=meme.description)
            await session.execute(stmt)
            await session.commit()
            
            
    @classmethod
    async def delete_meme(cls,id:int)-> None:
        async with session_factory() as session:
            stmt = delete(Meme).filter(Meme.id == id)
            await session.execute(stmt)
            await session.commit()
            
    