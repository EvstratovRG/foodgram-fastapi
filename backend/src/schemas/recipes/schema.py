from pydantic import BaseModel, StringConstraints
from typing import Annotated

from backend.src.schemas.users.schema import UserBaseSchema
from backend.src.schemas.base import BaseORMSchema


class RecipeIngredientSchema(BaseModel):
    recipe_id: int
    ingredient_id: int
    amount: int


class RecipeTagSchema(BaseModel):
    recipe_id: int
    tag_id: int


class BaseIngredientSchema(BaseModel):
    id: int
    name: Annotated(str, StringConstraints(max_length=200))
    measurement_unit: int


class BaseTagSchema(BaseModel):
    id: int
    name: Annotated(str, StringConstraints(max_length=200))
    slug: Annotated(str, StringConstraints(max_length=200))
    color: str


class RecipeBaseSchema(BaseORMSchema):
    name: Annotated(str, StringConstraints(max_length=50))
    text: str
    cooking_time: int
    image: str
    author_id: int
    author: UserBaseSchema
    tags: list[BaseTagSchema]
    ingredients: list[BaseIngredientSchema]


class Follow(BaseModel):
    user_id: int
    user: UserBaseSchema
    following_id: int
    following: UserBaseSchema


class PurchaseCart(BaseModel):
    user_id: int
    user: UserBaseSchema
    recipes_id: int
    recipe: RecipeBaseSchema


class Favorite(BaseModel):
    user_id: int
    user: UserBaseSchema
    recipes_id: int
    recipe: RecipeBaseSchema


class UserSchema(UserBaseSchema):
    recipes: list[RecipeBaseSchema]


class TagSchema(BaseTagSchema):
    recipes: RecipeBaseSchema


class IngredientSchema(BaseIngredientSchema):
    recipes: RecipeBaseSchema