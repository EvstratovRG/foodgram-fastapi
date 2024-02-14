from sqlalchemy import select, insert, func
from typing import TYPE_CHECKING, Any
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from fastapi import status
from src.queries import recipes as recipe_queries
from src.models.users import User
from src.models.recipes import (
    Ingredient,
    PurchaseCart,
    RecipeIngredient,
    Recipe,
)
from sqlalchemy.exc import SQLAlchemyError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def shopping_cart(
    user_id: int,
    session: 'AsyncSession'
) -> Any:
    cart_data = (
        select(
            Ingredient.name,
            Ingredient.measurement_unit,
            func.sum(
                RecipeIngredient.amount
            ).label('amount')
        ).join(
            RecipeIngredient,
            RecipeIngredient.ingredient_id == Ingredient.id
        ).join(
            Recipe, Recipe.id == RecipeIngredient.recipe_id
        ).join(
            PurchaseCart, PurchaseCart.recipe_id == Recipe.id
        ).join(
            User, User.id == PurchaseCart.user_id
        ).where(
            User.id == user_id
        ).group_by(
            Ingredient.name,
            Ingredient.measurement_unit
        )
    )
    result = await session.execute(cart_data)
    return result.fetchall()


async def add_to_shopping_cart(
    recipe_id: int,
    current_user_id: int,
    session: 'AsyncSession'
) -> Recipe | None:
    stmt = insert(PurchaseCart).values(
        recipe_id=recipe_id,
        user_id=current_user_id
    )
    try:
        cart = await session.scalars(stmt)
        if not cart:
            raise IntegrityError('Рецепт не был добавлен в корзину')
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc.orig),
        )
    await session.commit()
    recipe = await recipe_queries.get_recipe(session, recipe_id)
    return recipe


async def del_from_shopping_cart(
    recipe_id: int,
    current_user_id: int,
    session: 'AsyncSession'
) -> bool:
    cart = select(PurchaseCart).where(
        PurchaseCart.recipe_id == recipe_id,
        PurchaseCart.user_id == current_user_id
    )
    result = await session.scalars(cart)
    if result is None:
        return False
    try:
        await session.delete(result.first())
        await session.commit()
    except SQLAlchemyError:
        return False
    return True
