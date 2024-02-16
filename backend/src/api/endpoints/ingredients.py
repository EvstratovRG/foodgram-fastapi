from fastapi import APIRouter, Depends, Query, status
from typing import Any

from src.queries import ingredients as ingredient_queries
from src.schemas import recipes as ingredient_schemas
from config.db import get_async_session
from src.api.constants.summaries import ingredients as ingredient_summaries

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/ingredients", tags=["/ingredients"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ingredient_schemas.BaseIngredientSchema],
    summary=ingredient_summaries.get_list_of_ingredients
)
async def get_ingredients(
    name: str | None = Query(None),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    ingredients = await ingredient_queries.get_ingredients(
        session=session,
        name=name,
    )
    return ingredients


@router.get(
    "/{ingredient_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ingredient_schemas.BaseIngredientSchema,
    summary=ingredient_summaries.get_definite_ingredient
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
    return ingredient
