from src.models.recipes.models import Ingredient
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from config.db import AsyncSession


async def get_ingredient(
        session: 'AsyncSession',
        ingredient_id: int
        ) -> Ingredient | None:
    stmt = (
        select(Ingredient).select_from(Ingredient).where(
            Ingredient.id == ingredient_id
        ).options(
            joinedload(Ingredient.recipes),
        ),
    )
    result = await session.scalars(stmt)
    return result.first()


async def get_ingredients(session: 'AsyncSession') -> Sequence[Ingredient]:
    stmt = select(Ingredient)
    result = await session.scalars(stmt)
    return result.all()
