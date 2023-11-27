from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField
from backend.src.models.base import Base, TimeMixin, str_200
from typing import Annotated, TYPE_CHECKING
from sqlalchemy.sql.sqltypes import JSON
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from backend.src.models.users.models import User


intpk = Annotated[int, mapped_column(primary_key=True)]


class RecipeIngredient(TimeMixin, Base):
    __tablename__ = 'recipes_ingredients'

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey('recipes.id'),
        primary_key=True,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey('ingredients.id'),
        primary_key=True,
    )
    amount: Mapped[int] = mapped_column(Integer, default=1)


class RecipeTag(TimeMixin, Base):
    __tablename__ = 'recipes_tags'

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey('recipes.id'),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tags.id'),
        primary_key=True,
    )


class Ingredient(TimeMixin, Base):
    __tablename__ = "ingredients"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str_200]
    measurement_unit: Mapped[str_200 | None]
    recipes: Mapped[list['Recipe']] = relationship(
        'Recipe',
        secondary='recipes_ingredients',
        back_populates='ingredients',
    )


class Tag(TimeMixin, Base):
    __tablename__ = "tags"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str_200]
    slug: Mapped[str_200 | None]
    color: Mapped[str | None] = mapped_column(String(7))
    recipes: Mapped[list['Recipe']] = relationship(
        'Recipe',
        secondary='recipes_tags',
        back_populates='tags'
    )


class Follow(TimeMixin, Base):
    __tablename__ = "follows"
    __table_args__ = (
        UniqueConstraint(
            'follower_id',
            'following_id',
            name='unique_follower_to_following'
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    follower_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.id',
            ondelete="CASCADE",
        ),
    )
    follower: Mapped['User'] = relationship(
        'User',
        foreign_keys=[follower_id],
        back_populates='follower',
        lazy='joined',
    )
    following_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.id',
            ondelete="CASCADE"
        ),
    )
    following: Mapped['User'] = relationship(
        'User',
        foreign_keys=[following_id],
        back_populates='following',
        lazy='joined',
    )

    @validates('following')
    def validate_following(self, key, following):
        if following == self.user:
            raise IntegrityError('Нельзя подписываться на самого себя')
        return following


class PurchaseCart(TimeMixin, Base):
    __tablename__ = "purchase_carts"
    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'recipe_id',
            name='unique_recipe_carts_user_carts'
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
    )
    buyer: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='buyer',
    )
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recipes.id",
            ondelete="CASCADE"
        ),
    )
    cart_recipe: Mapped['Recipe'] = relationship(
        'Recipe',
        foreign_keys=[recipe_id],
        back_populates='cart_recipe',
    )


class Favorite(TimeMixin, Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'recipe_id',
            name='unique_recipe_favorites_user_favorites'
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
    )
    favor_user: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='favor_user',
    )
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recipes.id",
            ondelete="CASCADE"
        ),
    )
    favor_recipe: Mapped['Recipe'] = relationship(
        'Recipe',
        foreign_keys=[recipe_id],
        back_populates='favor_recipe',
    )


class Recipe(TimeMixin, Base):
    __tablename__ = "recipes"

    id: Mapped[intpk] = mapped_column(autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    text: Mapped[str | None] = mapped_column(Text, default=None)
    cooking_time: Mapped[int] = mapped_column(Integer, default=1)
    image: Mapped[JSON | None] = mapped_column(
        ImageField(
            upload_storage='/backend/media'
        ),
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete='CASCADE'
        ),
    )
    author: Mapped['User'] = relationship(
        'User',
        back_populates='recipes',
    )
    tags: Mapped[list["Tag"]] = relationship(
        uselist=True,
        secondary='recipes_tags',
        back_populates='recipes',
    )
    # uselist - аналог many = True
    ingredients: Mapped[list["Ingredient"]] = relationship(
        uselist=True,
        secondary='recipes_ingredients',
        back_populates='recipes',
    )
    cart_recipe = relationship(
        'PurchaseCart',
        foreign_keys=[PurchaseCart.recipe_id],
        back_populates='cart_recipe',
        lazy='joined',
    )
    favor_recipe = relationship(
        'Favorite',
        foreign_keys=[Favorite.recipe_id],
        back_populates='favor_recipe',
        lazy='joined',
    )
