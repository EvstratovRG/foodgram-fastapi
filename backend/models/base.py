import datetime

from sqlalchemy import DateTime, text
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    declared_attr
)


class Base(DeclarativeBase):
    __abstract__ = True


class TimeMixin:

    @declared_attr
    def created_at(self) -> Mapped[datetime.datetime]:
        return mapped_column(
            DateTime,
            server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        )

    @declared_attr
    def updated_at(self) -> Mapped[datetime.datetime]:
        return mapped_column(
            DateTime,
            server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        )
