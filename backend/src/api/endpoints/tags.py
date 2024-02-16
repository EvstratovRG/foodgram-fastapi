from fastapi import APIRouter, Depends, status
from typing import Any

from src.queries import tags as tag_queries
from src.schemas import recipes as tag_schemas
from config.db import get_async_session
from src.api.constants.summaries import tags as tag_summaries

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/tags", tags=["/tags"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[tag_schemas.BaseTagSchema],
    summary=tag_summaries.get_the_list_of_tags
)
async def get_tags(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    tags = await tag_queries.get_tags(
        session=session
    )
    return tags


@router.get(
    "/{tag_id}/",
    status_code=status.HTTP_200_OK,
    response_model=tag_schemas.BaseTagSchema,
    summary=tag_summaries.get_definite_tag
)
async def get_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    tag = await tag_queries.get_tag(
        tag_id=tag_id,
        session=session
    )
    if tag is None:
        return status.HTTP_404_NOT_FOUND
    return tag
