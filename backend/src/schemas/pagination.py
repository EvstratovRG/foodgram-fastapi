from pydantic import BaseModel
from typing import TypeVar

T = TypeVar('T')


class Links(BaseModel):
    next: str | None = None
    previous: str | None = None


class Pagination(BaseModel):
    count: int
    next: Links.next
    previous: Links.previous
    result: list[T]
