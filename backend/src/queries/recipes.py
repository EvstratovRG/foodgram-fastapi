from src.models.users.models import User
from src.schemas import recipes as recipes_schema
from src.models.recipes.models import (
    Recipe,
    RecipeIngredient,
    RecipeTag,
)
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload
from src.queries.ingredients import get_ingredient
from src.queries.tags import get_tag
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from src.api.base64_decoder import base64_decoder

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


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


async def create_or_update_through_entities(
        recipe: int,
        method,
        many_to_many_data: recipes_schema.IngredientAmount | list[int],
        model: RecipeIngredient | RecipeTag,
        session: 'AsyncSession'
        ) -> RecipeIngredient | RecipeTag:
    """Создание many-to-many сущностей."""
    # тут можно сделать булк, сущностей может быть много
    if model is RecipeIngredient:
        list_ingredients = []
        amounts = []
        for elem in many_to_many_data:
            data = dict(elem)
            through = method(model).values(
                recipe_id=recipe,
                ingredient_id=data.get('id'),
                amount=data.get('amount')
            )
            await session.execute(through)
            list_ingredients.append(
                await get_ingredient(
                    session,
                    data.get('id'),
                ),
            )
            amounts.append(data.get('amount'))
        validate_list_ingredients = [
            recipes_schema.IngredientThroughSchema(
                amount=amount,
                id=ingredient.id,
                name=ingredient.name,
                measurement_unit=ingredient.measurement_unit
            )
            for ingredient, amount in zip(list_ingredients, amounts)]
        return validate_list_ingredients
    else:
        list_tags = []
        for elem in many_to_many_data:
            through = method(model).values(
                recipe_id=recipe,
                tag_id=elem
            )
            await session.execute(through)  # нужно ли делать, если инсерт?
            list_tags.append(await get_tag(session, elem))
        validated_tags = [
            recipes_schema.BaseTagSchema.model_validate(tag)
            for tag in list_tags
        ]
        return validated_tags


async def create_recipe_entity(
        recipe_data: recipes_schema.CreateRecipeSchema,
        author: User,
        session: 'AsyncSession'
        ) -> Recipe:
    """Создание рецепта."""
    stmt = insert(Recipe).values(
        name=recipe_data.name,
        text=recipe_data.text,
        cooking_time=recipe_data.cooking_time,
        image=base64_decoder(recipe_data.image_incoded_base64),
        author_id=author.id,
        ).returning(Recipe).options(
            selectinload(Recipe.cart_recipe),
            selectinload(Recipe.favor_recipe),
        )
    try:
        result = await session.scalar(stmt)
        if not result:
            raise IntegrityError('Рецепт не создан')
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc.orig),
        )
    return result


async def create_recipe(
        session: 'AsyncSession',
        recipe_schema: recipes_schema.CreateRecipeSchema,
        author: User,
        ) -> recipes_schema.RecipeBaseSchema:
    """Создание рецепта со связанными сущностями."""
    recipe = await create_recipe_entity(recipe_schema, author, session)
    if recipe_schema.ingredients:
        list_ingredients = await create_or_update_through_entities(
            recipe=recipe.id,
            method=insert,
            many_to_many_data=recipe_schema.ingredients,
            model=RecipeIngredient,
            session=session
        )
    if recipe_schema.tags:
        list_tags = await create_or_update_through_entities(
            recipe=recipe.id,
            method=insert,
            many_to_many_data=recipe_schema.tags,
            model=RecipeTag,
            session=session
        )
    await session.commit()
    return recipes_schema.RecipeBaseSchema(
        id=recipe.id,
        name=recipe.name,
        text=recipe.text,
        cooking_time=recipe.cooking_time,
        image=recipe.image,
        author=author,
        tags=list_tags,
        ingredients=list_ingredients,
        is_favorited=recipe.is_favorited,
        is_in_shopping_cart=recipe.is_in_shopping_cart
    )


async def update_recipe(
        session: 'AsyncSession',
        recipe_id: int,
        author: User,
        recipe_schema: recipes_schema.CreateRecipeSchema
        ) -> recipes_schema.RecipeBaseSchema | None:
    """Обновление рецепта."""
    recipe = await get_recipe(session, recipe_id)
    if recipe is None:
        return None
    recipe.cooking_time = recipe_schema.cooking_time
    recipe.text = recipe_schema.text
    recipe.name = recipe_schema.name
    recipe.image = base64_decoder(recipe_schema.image_incoded_base64)
    recipe_tags = await create_or_update_through_entities(
        recipe=recipe_id,
        many_to_many_data=recipe_schema.tags,
        model=RecipeTag,
        method=update,
        session=session
    )
    recipe_ingredients = await create_or_update_through_entities(
        recipe=recipe_id,
        many_to_many_data=recipe_schema.ingredients,
        model=RecipeIngredient,
        method=update,
        session=session
    )
    await recipe.commit()
    return recipes_schema.RecipeBaseSchema(
        id=recipe_id,
        name=recipe.name,
        text=recipe.text,
        cooking_time=recipe.cooking_time,
        image=recipe.image,
        author=author,
        tags=recipe_tags,
        ingredients=recipe_ingredients,
        is_favorited=recipe.is_favorited,
        is_in_shopping_cart=recipe.is_in_shopping_cart
    )


async def delete_recipe(
        session: 'AsyncSession',
        recipe_id: int
        ) -> bool | None:
    """Удаление рецепта."""
    recipe = await get_recipe(session, recipe_id)
    if recipe is None:
        return None
    try:
        await session.delete(recipe)
        await session.commit()
    except SQLAlchemyError:
        return False
    return True
