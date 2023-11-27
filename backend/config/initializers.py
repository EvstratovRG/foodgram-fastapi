from fastapi import FastAPI


def init_app() -> FastAPI:
    from config import app_config

    app = FastAPI(**app_config)
    return app


def init_routers(application: FastAPI) -> None:
    from config.routers import get_routers
    from src.api.endpoints import auth as a
    from src.api.endpoints.auth import router as auth_router

    application.include_router(
        router=auth_router,
        prefix=a.auth_prefix,
        tags=a.tags)

    application.include_router(
        router=a.auth_router,
        prefix=a.auth_prefix,
        tags=a.tags,
    )
    application.include_router(
        router=a.register_router,
        prefix=a.prefix,
        tags=a.tags,
    )

    for router in get_routers():
        application.include_router(router, prefix='/api')
