from sqlalchemy.orm import Mapped,mapped_column

from .base import Base


class Meme(Base):
    __tablename__ = "memes"
    id:Mapped[int] = mapped_column(primary_key=True, unique=True,autoincrement=True)
    name:Mapped[str]
    description:Mapped[str]

