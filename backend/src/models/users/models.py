from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.src.models.base import Base, TimeMixin
from typing import Annotated
from backend.src.models.base import str_150
from backend.src.models.recipes.models import Recipe


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(TimeMixin, Base):
    __tablename__: str = "users"
    __table_args__ = (
        UniqueConstraint("username"),
    )

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    username: Mapped[str_150] = mapped_column(unique=True)
    first_name: Mapped[str_150 | None]
    last_name: Mapped[str_150 | None]
    email: Mapped[str_150]
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    recipes: Mapped[list['Recipe']] = relationship(uselist=True)
