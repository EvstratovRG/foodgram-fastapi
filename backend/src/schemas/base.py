from pydantic import BaseModel, ConfigDict

from src.api.constants.examples import auth as auth_examples


class BaseORMSchema(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StatusSchema(BaseModel):
    status_code: int
    is_deleted: bool


class DetailSchema(BaseModel):
    """Схема детального ответа."""
    detail: str


class ExceptionSchema(DetailSchema):
    status_code: int


class Token(BaseModel):
    auth_token: str


class AuthLoginSchema(BaseModel):
    email: str
    password: str

    model_config = auth_examples.post_roken_auth_example


class UpdatePasswordResponseSchema(ExceptionSchema):
    pass
