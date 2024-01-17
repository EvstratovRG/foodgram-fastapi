from typing import Any
from sqlalchemy import Select


def calculate_offset(limit: int, page: int) -> int:
    return (page - 1) * limit


def paginate(
    page: int | None,
    limit: int | None,
    statement: Select | None = None
) -> Any:
    if page is not None and limit is not None:
        offset = calculate_offset(limit=limit, page=page)
        return statement.limit(limit).offset(offset)
    return statement
