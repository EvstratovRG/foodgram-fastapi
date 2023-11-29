from datetime import timedelta
from fastapi import APIRouter, Depends
from src.auth.authorization import authenticate_user, create_access_token
from src.schemas import base as base_schemas
from config.db import get_async_session, AsyncSession
from src.api.exceptions.users import WrongСredentials
from config import app_config
from typing import Any

router = APIRouter(prefix="/auth/token", tags=["/auth/token"])


@router.post(
    "/login",
    response_model=base_schemas.Token
)
async def login_to_get_token(
    schema: base_schemas.AuthLoginSchema,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    user = await authenticate_user(
        email=schema.email,
        password=schema.password,
        session=session
    )
    if not user:
        raise WrongСredentials
    token_expire = timedelta(minutes=app_config.token_expire)
    token = create_access_token(
        data={'sub': user.email},
        expires_delta=token_expire,
    )
    return {'token': token}
