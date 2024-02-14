from src.models.recipes import Ingredient
from sqlalchemy import select
from src.schemas.recipes import CreateIngredientSchema
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_ingredient(
        session: 'AsyncSession',
        ingredient_id: int
        ) -> Ingredient | None:
    stmt = select(Ingredient).where(Ingredient.id == ingredient_id)
    result = await session.scalars(stmt)
    return result.first()


async def get_ingredients(session: 'AsyncSession') -> Sequence[Ingredient]:
    stmt = select(Ingredient)
    result = await session.scalars(stmt)
    return result.all()


async def post_ingredient(
        session: 'AsyncSession',
        ingredient_schema: CreateIngredientSchema
        ) -> Ingredient:
    ingredient = Ingredient(
        name=ingredient_schema.name,
        measurement_unit=ingredient_schema.measurement_unit,
    )
    try:
        session.add(ingredient)
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc.orig),
        )
    return ingredient
