from pydantic import BaseModel, StringConstraints, EmailStr
from typing import Annotated

str_150 = Annotated[str, StringConstraints(max_length=150)]
email_150 = Annotated[EmailStr, StringConstraints(max_length=150)]


class UserBaseSchema(BaseModel):
    id: int
    username: str_150
    first_name: str_150
    last_name: str_150
    email: email_150


class CreateUserSchema(BaseModel):
    username: str_150
    first_name: str_150
    last_name: str_150
    email: str_150


class UpdateUserSchema(CreateUserSchema):
    pass
