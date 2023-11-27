from pydantic import BaseModel, StringConstraints
from typing import Annotated

from src.schemas.users import UserBaseSchema
from src.schemas.base import BaseORMSchema


str_200 = Annotated[str, StringConstraints(max_length=200)]
str_50 = Annotated[str, StringConstraints(max_length=50)]


class RecipeIngredientSchema(BaseModel):
    recipe_id: int
    ingredient_id: int
    amount: int


class RecipeTagSchema(BaseModel):
    recipe_id: int
    tag_id: int


class BaseIngredientSchema(BaseModel):
    id: int
    name: str_200
    measurement_unit: int


class BaseTagSchema(BaseModel):
    id: int
    name: str_200
    slug: str_200
    color: str


class RecipeBaseSchema(BaseORMSchema):
    name: str_50
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
    recipe_id: int
    recipe: RecipeBaseSchema


class Favorite(BaseModel):
    user_id: int
    user: UserBaseSchema
    recipe_id: int
    recipe: RecipeBaseSchema


class UserSchema(UserBaseSchema):
    recipes: list[RecipeBaseSchema]


class TagSchema(BaseTagSchema):
    recipes: RecipeBaseSchema


class IngredientSchema(BaseIngredientSchema):
    recipes: RecipeBaseSchema
