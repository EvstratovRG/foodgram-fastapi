from backend.src.models.recipes.models import Tag
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from backend.config.db import AsyncSession


async def get_tag(
        session: 'AsyncSession',
        tag_id: int
        ) -> Tag | None:
    stmt = (
        select(Tag).select_from(Tag).where(Tag.id == tag_id).options(
            joinedload(Tag.recipes),
        ),
    )
    result = await session.scalars(stmt)
    return result.first()


async def get_tags(session: 'AsyncSession') -> Sequence[Tag]:
    stmt = select(Tag)
    result = await session.scalars(stmt)
    return result.all()
