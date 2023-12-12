from pydantic import BaseModel, StringConstraints, Field
from typing import Annotated

from src.schemas.users import UserBaseSchema
from src.schemas.base import BaseORMSchema

str_200 = Annotated[str, StringConstraints(max_length=200)]
str_50 = Annotated[str, StringConstraints(max_length=50)]


class RecipeIngredientSchema(BaseModel):
    recipe_id: int
    ingredient_id: int
    amount: int


class IngredientAmount(BaseModel):
    id: int
    amount: int


class RecipeTagSchema(BaseModel):
    recipe_id: int
    tag_id: int


class TagId(BaseModel):
    id: int


class BaseIngredientSchema(BaseORMSchema):
    name: str_200
    measurement_unit: str_200


class IngredientThroughSchema(BaseIngredientSchema):
    amount: int


class CreateIngredientSchema(BaseModel):
    name: str_200
    measurement_unit: str_200


class BaseTagSchema(BaseORMSchema):
    name: str_200
    slug: str_200
    color: str


class CreateTagSchema(BaseModel):
    name: str_200
    slug: str_200
    color: str


class RecipeBaseSchema(BaseORMSchema):
    name: str_200
    text: str
    cooking_time: int
    image: str
    author: UserBaseSchema
    tags: list[BaseTagSchema]
    ingredients: list[IngredientThroughSchema]
    is_favorited: bool = Field(default=False)
    is_in_shopping_cart: bool = Field(default=False)


class CreateRecipeSchema(BaseModel):
    name: str_50
    text: str
    cooking_time: int
    image_incoded_base64: str = Field(alias='image')
    tags: list[int]
    ingredients: list[IngredientAmount]


class UpdateRecipeSchema(CreateRecipeSchema):
    pass


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
