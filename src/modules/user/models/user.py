from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db import ModelBase


class User(ModelBase):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))  # noqa: WPS432
