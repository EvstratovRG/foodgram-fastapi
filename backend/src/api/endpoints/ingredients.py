from fastapi import APIRouter, Depends, Query, status
from typing import Any

from config.db import get_async_session
from src.queries import ingredients as ingredient_queries
from src.api.constants.summaries import ingredients as ingredient_summaries
from src.api.constants.responses import ingredients as ingredient_responses
from src.schemas import recipes as recipe_schemas
from src.api.exceptions import recipes as recipe_exceptions
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/ingredients", tags=["/ingredients"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses=ingredient_responses.get_ingredients,
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
    return [
        recipe_schemas.BaseIngredientSchema.model_validate(ingredient)
        for ingredient in ingredients
    ]


@router.get(
    "/{ingredient_id}/",
    status_code=status.HTTP_200_OK,
    responses=ingredient_responses.get_ingredient,
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
        raise recipe_exceptions.IngredientNotFound
    return recipe_schemas.BaseIngredientSchema.model_validate(ingredient)
