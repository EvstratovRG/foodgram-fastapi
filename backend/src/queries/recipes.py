from src.models.users.models import User
from src.schemas import recipes as recipes_schema
from src.models.recipes.models import Recipe, RecipeIngredient, RecipeTag, Ingredient, Tag
from src.queries.ingredients import get_ingredient
from src.queries.tags import get_tag
from sqlalchemy import select
# from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from config.db import AsyncSession


async def get_recipe(
        session: 'AsyncSession',
        recipe_id: int
        ) -> Recipe | None:
    stmt = select(Recipe).where(Recipe.id == recipe_id)
    result = await session.scalars(stmt)
    return result.first()


async def get_recipes(
        session: 'AsyncSession'
        ) -> Sequence[Recipe]:
    stmt = select(Recipe)
    result = await session.scalars(stmt)
    return result.all()


async def create_through_entities(
        recipe: int,
        data: recipes_schema.RecipeIngredientSchema,
        model: RecipeIngredient | RecipeTag,
        method: Ingredient | Tag | None,
        session: 'AsyncSession'
        ) -> RecipeIngredient | RecipeTag:
    for elem in data:
        entity: int = method(elem.id)
        if model is RecipeIngredient:
            through = model(recipe, entity, data.amount)
        through = model(recipe, entity)
        result = await session.add(through)
    return result


async def create_recipe_entity(
        recipe_data: recipes_schema.CreateRecipeSchema,
        author: User,
        session: 'AsyncSession'
        ) -> Recipe:
    recipe = Recipe(
        name=recipe_data.name,
        text=recipe_data.text,
        cooking_time=recipe_data.cooking_time,
        image=recipe_data.image,
        author=author
    )
    result = await session.add(recipe)
    await session.flush()
    return result


async def create_recipe(
        session: 'AsyncSession',
        recipe_schema: recipes_schema.CreateRecipeSchema,
        author: User,
        ) -> Recipe:
    recipe = await create_recipe_entity(recipe_schema, author, session)
    if recipe_schema.ingredients:
        await create_through_entities(
            recipe.id,
            recipe_schema.ingredients,
            RecipeIngredient,
            get_ingredient,
            session
        )
    if recipe_schema.tags:
        await create_through_entities(
            recipe.id,
            recipe_schema.tags,
            RecipeTag,
            get_tag,
            session
        )
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
