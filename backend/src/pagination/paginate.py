from typing import Any
from sqlalchemy import select, Select
from src.models.base import Base


def calculate_offset(limit: int, page: int) -> int:
    return (page - 1) * limit


def paginate(
    model: type[Base],
    page: int,
    limit: int,
    statement: Select | None = None
) -> Any:
    offset = calculate_offset(limit=limit, page=page)
    if statement is not None:
        stmt = statement.limit(limit).offset(offset)
        return stmt
    stmt = select(model).limit(limit).offset(offset)
    return stmt
