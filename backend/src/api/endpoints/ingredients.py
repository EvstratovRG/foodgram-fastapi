from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_async_session
from src.api.constants.responses import ingredients as ingredient_responses
from src.api.constants.summaries import ingredients as ingredient_summaries
from src.api.exceptions import recipes as recipe_exceptions
from src.queries import ingredients as ingredient_queries
from src.schemas import recipes as recipe_schemas

router = APIRouter(prefix="/ingredients", tags=["/ingredients"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses=ingredient_responses.get_ingredients,
    summary=ingredient_summaries.get_list_of_ingredients,
    response_model=list[recipe_schemas.BaseIngredientSchema]
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
    responses=ingredient_responses.get_ingredient,
    summary=ingredient_summaries.get_definite_ingredient,
    response_model=recipe_schemas.BaseIngredientSchema
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
        raise recipe_exceptions.IngredientNotFound
    return ingredient
