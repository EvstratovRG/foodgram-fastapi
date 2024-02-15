from pydantic import BaseModel, ConfigDict, Field, StringConstraints, EmailStr
from typing import Annotated
from src.schemas.base import BaseORMSchema


str_150 = Annotated[str, StringConstraints(max_length=150)]
email_150 = Annotated[EmailStr, StringConstraints(max_length=150)]


class UserBaseSchema(BaseORMSchema):

    username: str_150
    first_name: str_150
    last_name: str_150
    email: email_150
    is_subscribed: bool = Field(default=False)


class CreateUserSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username: str_150
    first_name: str_150
    last_name: str_150
    email: str_150
    password: str_150


class ChangeUserPassword(BaseModel):
    new_password: str_150
    current_password: str_150


class GetSubscriptions(UserBaseSchema):
    recipes: list['Subcriptions'] | None = None
    recipes_count: int | None = None


from src.schemas.recipes import Subcriptions

GetSubscriptions.model_rebuild()
