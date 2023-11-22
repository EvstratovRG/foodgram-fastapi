import datetime

from sqlalchemy import DateTime, String, text
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    declared_attr
)
from typing import Annotated

str_150 = Annotated[str, 150]
str_200 = Annotated[str, 200]


class Base(DeclarativeBase):
    """Декларативная Мета-дата."""
    type_annotation_map = {
        str_150: String(150),
        str_200: String(200)
    }


class TimeMixin:
    """Миксин времени создания и обновления."""

    @declared_attr
    def created_at(self) -> Mapped[datetime.datetime]:
        return mapped_column(
            DateTime,
            server_default=text("TIMEZONE('utc', now())"),
        )

    @declared_attr
    def updated_at(self) -> Mapped[datetime.datetime]:
        return mapped_column(
            DateTime,
            server_default=text("TIMEZONE('utc', now())"),
            onupdate=datetime.datetime.utcnow,
        )
