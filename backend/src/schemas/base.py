from pydantic import BaseModel, ConfigDict


class BaseORMSchema(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StatusSchema(BaseModel):
    success: bool


class DetailSchema(BaseModel):
    """Схема детального ответа."""
    detail: str