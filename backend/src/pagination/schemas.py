from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from src.schemas import recipes as recipe_schemas
from src.schemas import users as user_schemas

T = TypeVar('T')


class Pagination(BaseModel, Generic[T]):
    count: int
    next: str | None
    previous: str | None = None
    results: list[T] = Field([])


UserPagination = Pagination[user_schemas.UserBaseSchema]
SubscibePagination = Pagination[user_schemas.GetSubscriptions]
RecipePagination = Pagination[recipe_schemas.RecipeBaseSchema]
