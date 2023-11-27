from fastapi import APIRouter, FastAPI
from src.authentication.auth import auth_backend
from src.authentication.schemas import UserRead, UserCreate
from fastapi_users import FastAPIUsers
from src.models.users.models import User


from src.authentication.manager import get_user_manager

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
auth_router = fastapi_users.get_auth_router(auth_backend)
auth_prefix = "/jwt/auth"
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
prefix = "/auth"
tags = ["/auth"]

router = APIRouter()

current_user = fastapi_users.current_user()
