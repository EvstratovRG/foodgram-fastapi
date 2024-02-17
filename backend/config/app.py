from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def get_fastapi_app() -> FastAPI:
    from config.initializers import init_admin, init_app, init_routers

    application: FastAPI = init_app()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_routers(application)
    init_admin(application)

    return application
