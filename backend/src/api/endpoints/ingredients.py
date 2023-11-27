from fastapi import APIRouter, Depends, status
from typing import Any

from backend.src.queries import ingredients as ingredient_queries
from backend.src.schemas import recipes as ingredient_schemas
from backend.config.db import get_async_session, AsyncSession


router = APIRouter(prefix="/ingredients", tags=["/ingredients"])


@router.get(
    "/{ingredient_id}",
    status_code=status.HTTP_200_OK
)
async def get_ingredient(
    ingredient_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    ingredient = await ingredient_queries.get_ingredient(
        ingredient_id=ingredient_id,
        session=session
    )
    if ingredient is None:
        return status.HTTP_404_NOT_FOUND
    return ingredient_schemas.IngredientSchema.model_validate(ingredient)


@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_ingredients(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    ingredients = await ingredient_queries.get_ingredients(
        session=session
    )
    return (
        [ingredient_schemas.TagSchema.model_validate(ingredient)
         for ingredient in ingredients]
        )
