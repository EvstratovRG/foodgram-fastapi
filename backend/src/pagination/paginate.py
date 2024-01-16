from typing import Any
from sqlalchemy import select, Select
from src.models.base import Base


def calculate_offset(limit: int, page: int) -> int:
    return (page - 1) * limit


def paginate(
    model: type[Base] | None,
    page: int | None,
    limit: int | None,
    statement: Select | None = None
) -> Any:
    if page is not None and limit is not None:
        offset = calculate_offset(limit=limit, page=page)
        if statement is not None:
            return statement.limit(limit).offset(offset)
        return select(model).limit(limit).offset(offset)
    if model is not None:
        return select(model)
    if statement is not None:
        return select(statement)
