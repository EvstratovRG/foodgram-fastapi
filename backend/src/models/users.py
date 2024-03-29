from typing import TYPE_CHECKING, Annotated, Self

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimeMixin, str_150
from src.models.recipes import Favorite, Follow, PurchaseCart

if TYPE_CHECKING:
    from src.models.recipes import Recipe


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(TimeMixin, Base):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("username"),
    )

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    username: Mapped[str_150] = mapped_column(unique=True)
    first_name: Mapped[str_150 | None]
    last_name: Mapped[str_150 | None]
    email: Mapped[str_150] = mapped_column(
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str_150] = mapped_column(nullable=False)
    is_staff: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(
        String(250),
        nullable=True,
    )
    is_authenticated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    recipes: Mapped[list['Recipe']] = relationship(
        'Recipe',
        uselist=True,
        lazy='selectin',
    )
    follower: Mapped['Follow'] = relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        back_populates='follower',
        lazy='selectin',
        uselist=True
    )
    following: Mapped['Follow'] = relationship(
        'Follow',
        foreign_keys=[Follow.following_id],
        back_populates='following',
        lazy='selectin',
        uselist=True
    )
    buyer: Mapped['PurchaseCart'] = relationship(
        'PurchaseCart',
        foreign_keys=[PurchaseCart.user_id],
        back_populates='users',
        lazy='selectin',
        uselist=True,
    )
    favor_user: Mapped['Favorite'] = relationship(
        'Favorite',
        foreign_keys=[Favorite.user_id],
        back_populates='favor_user',
        lazy='selectin',
        uselist=True
    )

    @hybrid_property
    def is_subscribed(self: Self) -> bool:
        return bool(self.follower)

    @hybrid_property
    def recipes_count(self: Self) -> int:
        return len(self.recipes)

    def __str__(self) -> str:
        return f'{self.username}, {self.email}'
