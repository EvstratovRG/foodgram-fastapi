from pydantic import BaseModel
from typing import Generic, TypeVar


T = TypeVar('T')


class Pagination(BaseModel, Generic[T]):
    count: int
    next: str | None
    previous: str | None = None
    result: list[T]
