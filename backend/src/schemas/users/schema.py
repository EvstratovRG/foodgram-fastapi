from pydantic import BaseModel, StringConstraints
from typing import Annotated


class UserBaseSchema(BaseModel):
    id: int
    username: Annotated(str, StringConstraints(max_length=150))
    first_name: Annotated(str, StringConstraints(max_length=150))
    last_name: Annotated(str, StringConstraints(max_length=150))
    email: Annotated(str, StringConstraints(max_length=150))
    is_staff: bool
    is_active: bool
