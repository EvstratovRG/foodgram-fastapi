from sqlalchemy import Boolean, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.models.base import Base, TimeMixin
from typing import Annotated, TYPE_CHECKING
from src.models.base import str_150
# from backend.src.models.permissions import UserPermissions
from src.models.recipes.models import Follow, PurchaseCart, Favorite
from fastapi_users.db import SQLAlchemyBaseUserTable

if TYPE_CHECKING:
    from src.models.recipes.models import Recipe


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(SQLAlchemyBaseUserTable, TimeMixin, Base):
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
    password: Mapped[str_150] = mapped_column(nullable=False)
    is_staff: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
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
    recipes: Mapped[list['Recipe']] = relationship(uselist=True)
    follower = relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        back_populates='follower',
        lazy='joined',
    )
    following = relationship(
        'Follow',
        foreign_keys=[Follow.following_id],
        back_populates='following',
        lazy='joined',
    )
    buyer = relationship(
        'PurchaseCart',
        foreign_keys=[PurchaseCart.user_id],
        back_populates='buyer',
        lazy='joined',
    )
    favor_user = relationship(
        'Favorite',
        foreign_keys=[Favorite.user_id],
        back_populates='favor_user',
        lazy='joined',
    )
