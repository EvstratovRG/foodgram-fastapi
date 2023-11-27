from fastapi import APIRouter, Depends, status
from typing import Any

from src.queries import tags as tag_queries
from src.schemas import recipes as tag_schemas
from config.db import get_async_session, AsyncSession


router = APIRouter(prefix="/tags", tags=["/tags"])


@router.get(
    "/{tag_id}",
    status_code=status.HTTP_200_OK
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
    return tag_schemas.TagSchema.model_validate(tag)


@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_tags(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    tags = await tag_queries.get_tags(
        session=session
    )
    return [tag_schemas.TagSchema.model_validate(tag) for tag in tags]
