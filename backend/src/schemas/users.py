from pydantic import BaseModel, ConfigDict, StringConstraints, EmailStr
from typing import Annotated

str_150 = Annotated[str, StringConstraints(max_length=150)]
email_150 = Annotated[EmailStr, StringConstraints(max_length=150)]


class UserBaseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str_150
    first_name: str_150
    last_name: str_150
    email: email_150


class CreateUserSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username: str_150
    first_name: str_150
    last_name: str_150
    email: str_150
    password: str_150


class UpdateUserSchema(CreateUserSchema):
    pass
