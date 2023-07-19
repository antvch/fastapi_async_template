from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String
from src.db import ModelBase

class User(ModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))