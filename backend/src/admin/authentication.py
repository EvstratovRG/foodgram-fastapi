from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi import FastAPI
from backend.config.db import async_engine

app = FastAPI()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="12345")
admin = Admin(
    app=app,
    engine=async_engine,
    authentication_backend=authentication_backend
)
