from src.models.recipes.models import Tag
from sqlalchemy import select
# from sqlalchemy.orm import joinedload
from src.schemas.recipes import CreateTagSchema
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from fastapi import status

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from config.db import AsyncSession


async def get_tag(
        session: 'AsyncSession',
        tag_id: int
        ) -> Tag | None:
    # stmt = (
    #     select(Tag).select_from(Tag).where(Tag.id == tag_id).options(
    #         joinedload(Tag.recipes),
    #     ),
    # )
    stmt = select(Tag).where(Tag.id == tag_id)
    result = await session.scalars(stmt)
    return result.first()


async def get_tags(session: 'AsyncSession') -> Sequence[Tag]:
    stmt = select(Tag)
    result = await session.scalars(stmt)
    return result.all()


async def post_tag(
        session: 'AsyncSession',
        tag_schema: CreateTagSchema
        ) -> Tag:
    tag = Tag(
        name=tag_schema.name,
        slug=tag_schema.slug,
        color=tag_schema.color
    )
    try:
        session.add(tag)
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc.orig),
        )
    return tag
