from fastapi import APIRouter, Depends, Query, status, Request
from typing import Any
from src.pagination.links import LinkCreator
from src.api.endpoints.users import get_me
from src.models.users import User
from src.queries import recipes as recipe_queries
from src.schemas import recipes as recipe_schemas
from src.pagination import schemas as pagination_schema
from src.schemas import base as base_schemas
from src.api.exceptions.recipes import (
    RecipeNotFoundException,
    SomethingGoesWrong
)
from config.db import get_async_session
from src.api.constants.summaries import recipes as recipes_summaries

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/recipes", tags=["/recipes"])
RecipePagination = pagination_schema.Pagination[
    recipe_schemas.RecipeBaseSchema
]


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=RecipePagination,
    summary=recipes_summaries.get_paginated_list_of_recipes
)
async def get_recipes(
    request: Request,
    page: int = Query(None),
    limit: int = Query(None),
    is_favorited: int = Query(None),
    is_in_shopping_cart: int = Query(None),
    tags: list[str] = Query(None),
    author: int = Query(None),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    if is_favorited is not None or is_in_shopping_cart is not None:
        is_favorited = bool(is_favorited)
        is_in_shopping_cart = bool(is_in_shopping_cart)
    count = await recipe_queries.get_recipes_count(
        is_favorited,
        is_in_shopping_cart,
        session=session,
    )
    recipes = await recipe_queries.get_recipes(
        page=page,
        limit=limit,
        tags=tags,
        author=author,
        is_favorited=is_favorited,
        is_in_shopping_cart=is_in_shopping_cart,
        session=session
    )
    if recipes is None:
        raise SomethingGoesWrong
    recipe_schemas_list = []
    for r in recipes:
        r_schema = recipe_schemas.RecipeBaseSchema.model_validate(r)
        r_schema.image_convert(request)
        recipe_schemas_list.append(r_schema)

    links = LinkCreator.generate_links(
        page=page,
        limit=limit,
        total=count,
        request=request
    )
    return RecipePagination(
        count=count,
        results=recipe_schemas_list,
        **links
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=recipe_schemas.RecipeBaseSchema,
    summary=recipes_summaries.create_recipe
)
async def create_recipe(
    recipe_schema: recipe_schemas.CreateRecipeSchema,
    author: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    created_recipe: recipe_schemas.RecipeBaseSchema = (
        await recipe_queries.create_recipe(
            session=session,
            recipe_schema=recipe_schema,
            author=author,
        )
    )
    return created_recipe


@router.get(
    "/{recipe_id}/",
    status_code=status.HTTP_200_OK,
    response_model=recipe_schemas.RecipeBaseSchema,
    summary=recipes_summaries.get_definite_recipe
)
async def get_recipe(
    request: Request,
    recipe_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    recipe = await recipe_queries.get_recipe(
        recipe_id=recipe_id,
        session=session
    )
    if recipe is None:
        raise RecipeNotFoundException
    r_schema = recipe_schemas.RecipeBaseSchema.model_validate(recipe)
    r_schema.image_convert(request)
    return r_schema


@router.patch(
    "/{recipe_id}/",
    status_code=status.HTTP_200_OK,
    response_model=recipe_schemas.RecipeBaseSchema,
    summary=recipes_summaries.update_definite_recipe
)
async def update_recipe(
    recipe_id: int,
    recipe_schema: recipe_schemas.UpdateRecipeSchema,
    author: User = Depends(get_me),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    updated_recipe = await recipe_queries.update_recipe(
        session=session,
        recipe_id=recipe_id,
        author=author,
        recipe_schema=recipe_schema
    )
    if not updated_recipe:
        return status.HTTP_404_NOT_FOUND
    return updated_recipe


@router.delete(
    "/{recipe_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=base_schemas.StatusSchema,
    summary=recipes_summaries.delete_definite_recipe
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
    return deleted_recipe
