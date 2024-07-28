from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict


class MemeCreate(BaseModel):
    """Схема, по которой API принимает от клиента файл
    (здесь create и update понятия полиморфные)"""
    file:UploadFile
    description:str


class MemeCreateOrm(BaseModel):
    """Схема, по которой мы добавляем новый файл в БД"""
    name:str
    description:str


class MemeDB(BaseModel):
    """Схема, по которой мы получаем ответ от БД"""
    id: int
    name: str
    description:str
    url: str = None
    model_config = ConfigDict(from_attributes=True)
