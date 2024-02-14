from src.models.users import User
from src.schemas import recipes as recipes_schema
from src.models.recipes import (
    Recipe,
    RecipeIngredient,
    RecipeTag,
    Tag,
)
from sqlalchemy import select, insert, func
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.orm import selectinload
from src.queries.ingredients import get_ingredient
from src.queries.tags import get_tag
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError
from src.api.base64_decoder import base64_decoder
from src.pagination.paginate import paginate

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_recipe(
        session: 'AsyncSession',
        recipe_id: int
        ) -> Recipe | None:
    stmt = select(Recipe).where(Recipe.id == recipe_id)
    result = await session.scalars(stmt)
    return result.unique().first()


async def get_recipes_count(
        session: 'AsyncSession'
) -> int:
    stmt = select(func.count()).select_from(Recipe)
    result = await session.scalar(stmt)
    return result


async def get_recipes(
        session: 'AsyncSession',
        tags: list[str] | None,
        author: int | None,
        page: int | None,
        limit: int | None,
        is_favorited: int | None,
        is_in_shopping_cart: int | None,
        ) -> Sequence[Recipe]:
    is_favorited = bool(is_favorited)
    is_in_shopping_cart = bool(is_in_shopping_cart)
    # если добавить в избранные или в шоппинг карт, рецепты не отображаются
    stmt = select(Recipe).where(
        Recipe.is_favorited == is_favorited,
        Recipe.is_in_shopping_cart == is_in_shopping_cart
    )
    if author is not None:
        stmt = stmt.where(
            Recipe.author_id == author
        )
    if tags is not None and tags != []:
        stmt = stmt.join(Recipe.tags).where(
            Tag.slug.in_(tags),
        )
    paginate_stmt = paginate(page=page, limit=limit, statement=stmt)
    result = await session.scalars(paginate_stmt)
    return result.unique().all()


async def create_recipe_ingredient_entities(
        recipe: int,
        many_to_many_data: recipes_schema.IngredientAmount,
        session: 'AsyncSession'
) -> recipes_schema.IngredientThroughSchema:
    """Создать RecipeIngredient."""
    ingredients = []
    amounts = []
    for elem in many_to_many_data:
        data = dict(elem)
        stmt = insert(RecipeIngredient).values(
            recipe_id=recipe,
            ingredient_id=data.get('id'),
            amount=data.get('amount')
        )
        await session.execute(stmt)
        ingredients.append(
            await get_ingredient(session, data.get('id')),
        )
        amounts.append(data.get('amount'))
    validate_list_ingredients = [
        recipes_schema.IngredientThroughSchema(
            amount=amount,
            id=ingredient.id,
            name=ingredient.name,
            measurement_unit=ingredient.measurement_unit
        )
        for ingredient, amount in zip(ingredients, amounts)]
    return validate_list_ingredients


async def create_recipe_tag_entities(
        recipe: int,
        many_to_many_data: list[int],
        session: 'AsyncSession'
) -> recipes_schema.BaseTagSchema:
    """Создать RecipeTag."""
    tags = []
    for elem in many_to_many_data:
        through = insert(RecipeTag).values(
            recipe_id=recipe,
            tag_id=elem
        )
        await session.execute(through)
        tags.append(
            await get_tag(session, elem)
        )
    validated_tags = [
        recipes_schema.BaseTagSchema.model_validate(tag)
        for tag in tags
    ]
    return validated_tags


async def update_recipe_ingredient_entities(
        recipe: int,
        many_to_many_data: recipes_schema.IngredientAmount,
        session: 'AsyncSession'
) -> recipes_schema.IngredientThroughSchema:
    """Обновить RecipeIngredient."""
    ingredients = []
    amounts = []
    for elem in many_to_many_data:
        data = dict(elem)
        stmt = upsert(
            RecipeIngredient
            ).values(
                recipe_id=recipe,
                ingredient_id=data.get('id'),
                amount=data.get('amount')
            )
        query = stmt.on_conflict_do_nothing()
        await session.execute(query)
        ingredients.append(
            await get_ingredient(session, data.get('id'))
        )
        amounts.append(data.get('amount'))
        validate_list_ingredients = [
            recipes_schema.IngredientThroughSchema(
                amount=amount,
                id=ingredient.id,
                name=ingredient.name,
                measurement_unit=ingredient.measurement_unit
            )
            for ingredient, amount in zip(ingredients, amounts)]
        return validate_list_ingredients


async def update_recipe_tag_entities(
        recipe: int,
        many_to_many_data: list[int],
        session: 'AsyncSession'
) -> recipes_schema.IngredientAmount:
    """Обновить RecipeIngredient."""
    tags = []
    for elem in many_to_many_data:
        stmt = upsert(
            RecipeTag
            ).values(
                recipe_id=recipe,
                tag_id=elem
            )
        query = stmt.on_conflict_do_nothing()
        await session.execute(query)
        tags.append(
            await get_tag(session, elem)
        )
    validated_tags = [
        recipes_schema.BaseTagSchema.model_validate(tag)
        for tag in tags
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
        list_ingredients = await create_recipe_ingredient_entities(
            recipe=recipe.id,
            many_to_many_data=recipe_schema.ingredients,
            session=session
        )
    if recipe_schema.tags:
        list_tags = await create_recipe_tag_entities(
            recipe=recipe.id,
            many_to_many_data=recipe_schema.tags,
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


async def update_recipe_entity(
        session: 'AsyncSession',
        recipe_id: int,
        recipe_schema: recipes_schema.CreateRecipeSchema
) -> Recipe:
    recipe = await get_recipe(session, recipe_id)
    if recipe is None:
        return None
    recipe.cooking_time = recipe_schema.cooking_time
    recipe.text = recipe_schema.text
    recipe.name = recipe_schema.name
    recipe.image = base64_decoder(recipe_schema.image_incoded_base64)
    return recipe


async def update_recipe(
        session: 'AsyncSession',
        recipe_id: int,
        author: User,
        recipe_schema: recipes_schema.CreateRecipeSchema
        ) -> recipes_schema.RecipeBaseSchema | None:
    """Обновление рецепта и его связанных атрибутов."""
    recipe = await update_recipe_entity(session, recipe_id, recipe_schema)
    recipe_tags = await update_recipe_tag_entities(
        recipe.id,
        recipe_schema.tags,
        session
    )
    recipe_ingredients = await update_recipe_ingredient_entities(
        recipe.id,
        recipe_schema.ingredients,
        session
    )
    await session.commit()
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
