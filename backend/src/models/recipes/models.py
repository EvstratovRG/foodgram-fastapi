from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField
from backend.src.models.base import Base, TimeMixin, str_200
from typing import Annotated
from backend.src.models.users.models import User


intpk = Annotated[int, mapped_column(primary_key=True)]


class RecipeIngredient(TimeMixin, Base):
    __tablename__: str = 'recipes_ingredients'

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
    __tablename__: str = 'recipes_tags'

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey('recipes.id'),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tags.id'),
        primary_key=True,
    )


class Ingredient(TimeMixin, Base):
    __tablename__: str = "ingredients"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str_200]
    measurement_unit: Mapped[str_200 | None]
    recipes: Mapped[list['Recipe']] = relationship(
        'Recipe',
        secondary='recipes_ingredients',
        back_populates='ingredients',
    )


class Tag(TimeMixin, Base):
    __tablename__: str = "tags"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str_200]
    slug: Mapped[str_200 | None]
    color: Mapped[str | None] = mapped_column(String(7))
    recipes: Mapped[list['Recipe']] = relationship(
        'Recipe',
        secondary='recipes_tags',
        back_populates='tags'
    )


class Recipe(TimeMixin, Base):
    __tablename__: str = "recipes"

    id: Mapped[intpk] = mapped_column(autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    text: Mapped[str | None] = mapped_column(Text, default=None)
    cooking_time: Mapped[int] = mapped_column(Integer, default=1)
    image: Mapped[str | None] = mapped_column(
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


class Follow(TimeMixin, Base):
    __tablename__: str = "followers"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.id',
            ondelete="CASCADE"
        ),
    )
    user: Mapped['User'] = relationship('User')
    following_id: Mapped[int] = mapped_column(
        ForeignKey(
            'users.id',
            ondelete="CASCADE"
        ),
    )
    following: Mapped['User'] = relationship('User')


class PurchaseCart(TimeMixin, Base):
    __tablename__: str = "purchase_carts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
    )
    user: Mapped['User'] = relationship('User')
    recipes_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recipes.id",
            ondelete="CASCADE"
        ),
    )
    recipe: Mapped['Recipe'] = relationship('Recipe')


class Favorite(TimeMixin, Base):
    __tablename__: str = "favorites"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
    )
    user: Mapped['User'] = relationship('User')
    recipes_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recipes.id",
            ondelete="CASCADE"
        ),
    )
    recipe: Mapped['Recipe'] = relationship('Recipe')
