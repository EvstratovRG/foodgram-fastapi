from src.models.recipes import Ingredient
from sqlalchemy import select


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


async def get_ingredients(
        session: 'AsyncSession',
        name: str | None = None
) -> Sequence[Ingredient]:
    stmt = select(Ingredient)
    if name:
        stmt = stmt.where(Ingredient.name.ilike(name + '%'))
    result = await session.scalars(stmt)
    return result.all()
