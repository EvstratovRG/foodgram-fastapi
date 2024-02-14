from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.models.base import Base, TimeMixin, str_200
from typing import Annotated, TYPE_CHECKING, Self
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property

if TYPE_CHECKING:
    from src.models.users.models import User


intpk = Annotated[int, mapped_column(primary_key=True)]


class RecipeIngredient(TimeMixin, Base):
    """Сквозная модель Рецепта и Ингредиентов
    для хранения many-to-many связи."""
    __tablename__ = 'recipe_ingredient'

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey('recipe.id'),
        primary_key=True,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey('ingredient.id'),
        primary_key=True,
    )
    amount: Mapped[int] = mapped_column(Integer, default=1)

    def __str__(self) -> str:
        return (
            f'id Рецепта{self.recipe_id}, '
            f'id Ингредиента{self.ingredient_id} '
            f'- кол-во {self.amount}'
        )


class RecipeTag(TimeMixin, Base):
    """Сквозная модель Рецепта и Тегов для хранения many-to-many связи."""
    __tablename__ = 'recipe_tag'

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey('recipe.id'),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tag.id'),
        primary_key=True,
    )

    def __str__(self) -> str:
        return (
            f'id Рецепта{self.recipe_id}, '
            f'id Тега{self.tag_id} '
        )


class Ingredient(TimeMixin, Base):
    """Модель данных хранения Ингредиентов."""
    __tablename__ = "ingredient"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str_200] = mapped_column(String, unique=True)
    measurement_unit: Mapped[str_200 | None]
    recipes: Mapped[list['Recipe']] = relationship(
        secondary='recipe_ingredient',
    )
    recipe_ingredient: Mapped[list['RecipeIngredient']] = relationship(
        uselist=True,
        lazy='selectin',
    )

    @hybrid_property
    def amount(self):
        return self.recipe_ingredient[0].amount

    def __str__(self):
        return f'{self.id}, {self.name}, {self.measurement_unit}'


class Tag(TimeMixin, Base):
    """Модель данных храненения Тэгов."""
    __tablename__ = "tag"

    id: Mapped[intpk] = mapped_column(autoincrement=True)
    name: Mapped[str_200] = mapped_column(String, unique=True)
    slug: Mapped[str_200 | None]
    color: Mapped[str | None] = mapped_column(String(7))
    recipes: Mapped[list['Recipe']] = relationship(
        secondary='recipe_tag',
    )

    def __str__(self):
        return f'{self.id}, {self.name}, {self.color}'


class Follow(TimeMixin, Base):
    """Модель данных хранения связей - Подписок пользователей."""
    __tablename__ = "follow"
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
            'user.id',
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
            'user.id',
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

    def __str__(self):
        return f'{self.id}, {self.follower}, {self.following}'


class PurchaseCart(TimeMixin, Base):
    """Модель хранения данных о Корзине товаров пользователя."""
    __tablename__ = "purchase_cart"
    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'recipe_id',
            name='unique_recipe_cart_user_cart'
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="CASCADE"
        ),
    )
    users: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='buyer',
    )
    recipe_id: Mapped[int] = mapped_column(
        ForeignKey(
            "recipe.id",
            ondelete="CASCADE"
        ),
    )
    recipe: Mapped['Recipe'] = relationship(
        'Recipe',
        foreign_keys=[recipe_id],
        back_populates='cart_recipe',
    )

    def __str__(self):
        return f'{self.id}, {self.users}, {self.recipe}'


class Favorite(TimeMixin, Base):
    """Модель данных хранения Избранных рецептов пользователя."""
    __tablename__ = "favorite"
    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'recipe_id',
            name='unique_recipe_favorite_user_favorite'
        ),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user.id",
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
            "recipe.id",
            ondelete="CASCADE"
        ),
    )
    favor_recipe: Mapped['Recipe'] = relationship(
        'Recipe',
        foreign_keys=[recipe_id],
        back_populates='favor_recipe',
    )

    def __str__(self):
        return f'{self.id}, {self.favor_user}, {self.favor_recipe}'


class Recipe(TimeMixin, Base):
    """Модель данных хранения Рецептов."""
    __tablename__ = "recipe"

    id: Mapped[intpk] = mapped_column(autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    text: Mapped[str | None] = mapped_column(Text, default=None)
    cooking_time: Mapped[int] = mapped_column(Integer, default=1)
    image: Mapped[str | None] = mapped_column(String())
    author_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete='CASCADE'
        ),
    )
    author: Mapped['User'] = relationship(
        'User',
        back_populates='recipes',
        lazy='joined',
    )
    tags: Mapped[list["Tag"]] = relationship(
        uselist=True,
        secondary='recipe_tag',
        lazy='joined',
    )
    ingredients: Mapped[list["Ingredient"]] = relationship(
        uselist=True,
        secondary='recipe_ingredient',
        lazy='joined',
    )
    cart_recipe: Mapped['PurchaseCart'] = relationship(
        'PurchaseCart',
        foreign_keys=[PurchaseCart.recipe_id],
        back_populates='recipe',
        lazy='joined',
    )
    favor_recipe: Mapped['Favorite'] = relationship(
        'Favorite',
        foreign_keys=[Favorite.recipe_id],
        back_populates='favor_recipe',
        lazy='joined',
    )

    @hybrid_property
    def is_in_shopping_cart(self: Self) -> bool:
        return bool(self.cart_recipe)

    @hybrid_property
    def is_favorited(self: Self) -> bool:
        return bool(self.favor_recipe)

    @is_favorited.expression
    @classmethod
    def is_favorited(cls):
        return cls.favor_recipe.has(recipe_id=cls.id)

    @is_in_shopping_cart.expression
    @classmethod
    def is_in_shopping_cart(cls):
        return cls.cart_recipe.has(recipe_id=cls.id)

    def __str__(self):
        return f'{self.id}, {self.name}, {self.author}'
