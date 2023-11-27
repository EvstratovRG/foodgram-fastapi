from fastapi import APIRouter, Depends, status
from typing import Any

from backend.src.queries import recipes as recipe_queries
from backend.src.schemas import recipes as recipe_schemas
from backend.src.schemas import base as base_schemas
from backend.config.db import get_async_session, AsyncSession


router = APIRouter(prefix="/recipes", tags=["/recipes"])


@router.get(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK
)
async def get_recipe(
    recipe_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    recipe = await recipe_queries.get_recipe(
        recipe_id=recipe_id,
        session=session
    )
    if recipe is None:
        return status.HTTP_404_NOT_FOUND
    return recipe_schemas.RecipeBaseSchema.model_validate(recipe)


@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_recipes(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    recipes = await recipe_queries.get_recipes(
        session=session
    )
    return [recipe_schemas.RecipeBaseSchema.model_validate(recipe) for recipe in recipes]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_recipe(
    recipe_schema: recipe_schemas.RecipeBaseSchema,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    created_recipe = await recipe_queries.create_recipe(
        session=session,
        recipe_schema=recipe_schema
    )
    return recipe_schemas.RecipeBaseSchema.model_validate(created_recipe)


@router.put(
    "/{recipe_id}",
    status_code=status.HTTP_200_OK
)
async def update_recipe(
    recipe_id: int,
    recipe_schema: recipe_schemas.RecipeBaseSchema,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    updated_recipe = await recipe_queries.update_recipe(
        session=session,
        recipe_id=recipe_id,
        recipe_schema=recipe_schema
    )
    if not updated_recipe:
        return status.HTTP_404_NOT_FOUND
    return recipe_schemas.RecipeBaseSchema.model_validate(updated_recipe)


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_202_ACCEPTED
)
async def delete_recipe(
    recipe_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    deleted_recipe = await recipe_queries.delete_recipe(
        session=session,
        recipe_id=recipe_id
    )
    if not deleted_recipe:
        return status.HTTP_404_NOT_FOUND
    return base_schemas.StatusSchema(success=deleted_recipe)
