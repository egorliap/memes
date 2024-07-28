from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self)->str:
        """Создает URL для асинхронного подключения к БД проекта из данных в pg.env"""        
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings(DB_HOST=os.getenv("DB_HOST"),
                    DB_PORT=os.getenv("DB_PORT"),
                    DB_USER=os.getenv("DB_USER"),
                    DB_PASS=os.getenv("DB_PASS"),
                    DB_NAME=os.getenv("DB_NAME"))
