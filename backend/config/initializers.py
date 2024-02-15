from fastapi import FastAPI
from sqladmin import Admin
from fastapi.staticfiles import StaticFiles


def init_app() -> FastAPI:
    from config import get_app_config

    app_config = get_app_config()

    app = FastAPI(
        **app_config.model_dump(),
        docs_url='/api/fastapi-docs/',
        openapi_url="/api/openapi.json",
        redoc_url=None
    )
    # путь для локальной разработки
    # app.mount(
    #     path="/static",
    #     app=StaticFiles(directory="backend/static/"),
    #     name="static"
    # )
    app.mount(
        path="/static",
        app=StaticFiles(directory="static/"),
        name="static"
    )

    return app


def init_routers(application: FastAPI) -> None:
    from config.routers import get_routers

    for router in get_routers():
        application.include_router(router, prefix='/api')


def init_admin(application: FastAPI) -> None:
    from config.db import sync_engine
    from config import site_config
    from src.admin.models import (
        UserAdmin,
        RecipeAdmin,
        TagAdmin,
        IngredientAdmin,
        FollowAdmin,
        FavoriteAdmin,
        PurchaseCartAdmin,
    )
    from src.admin.authentication import AdminAuth
    authentication_backend = AdminAuth(secret_key=site_config.host)
    admin = Admin(
        application,
        sync_engine,
        authentication_backend=authentication_backend
    )
    admin.add_view(UserAdmin)
    admin.add_view(RecipeAdmin)
    admin.add_view(TagAdmin)
    admin.add_view(IngredientAdmin)
    admin.add_view(FollowAdmin)
    admin.add_view(FavoriteAdmin)
    admin.add_view(PurchaseCartAdmin)
