from src.models.recipes import Tag
from sqlalchemy import select


from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from config.db import AsyncSession


async def get_tag(
        tag_id: int,
        session: 'AsyncSession'
        ) -> Tag | None:
    stmt = select(Tag).where(Tag.id == tag_id)
    result = await session.scalars(stmt)
    return result.first()


async def get_tags(
        session: 'AsyncSession'
        ) -> Sequence[Tag]:
    stmt = select(Tag)
    result = await session.scalars(stmt)
    return result.all()
