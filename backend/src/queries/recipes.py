from backend.src.schemas import recipes as recipes_schema
from backend.src.models.recipes.models import Recipe
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from backend.config.db import AsyncSession


async def get_recipe(
        session: 'AsyncSession',
        recipe_id: int
        ) -> Recipe | None:
    stmt = (
        select(Recipe).select_from(Recipe).where(
            Recipe.id == recipe_id).options(
            joinedload(Recipe.recipes),
        ),
    )
    result = await session.scalars(stmt)
    return result.first()


async def get_recipes(session: 'AsyncSession') -> Sequence[Recipe]:
    stmt = select(Recipe)
    result = await session.scalars(stmt)
    return result.all()


async def create_recipe(
        session: 'AsyncSession',
        recipe_schema: recipes_schema.RecipeBaseSchema
        ) -> Recipe:
    recipe = Recipe(
        username=recipe_schema.username,
        first_name=recipe_schema.first_name,
        last_name=recipe_schema.last_name,
        email=recipe_schema.email,
    )
    session.add(recipe)
    await session.commit()
    return recipe


async def update_recipe(
        session: 'AsyncSession',
        recipe_id: int,
        recipe_schema: recipes_schema.RecipeBaseSchema
        ) -> Recipe | None:
    recipe = await get_recipe(session, recipe_id)
    if recipe is None:
        return None
    recipe.username = recipe_schema.username
    recipe.first_name = recipe_schema.first_name
    recipe.last_name = recipe_schema.last_name
    recipe.email = recipe_schema.email
    await recipe.commit()
    return recipe


async def delete_recipe(
        session: 'AsyncSession',
        recipe_id: int
        ) -> bool | None:
    recipe = await get_recipe(session, recipe_id)
    if recipe is None:
        return None
    try:
        await session.delete(recipe)
        await session.commit()
    except SQLAlchemyError:
        return False
    return True
