from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


origins = ['*']


def get_fastapi_app() -> FastAPI:
    from config.initializers import (
        init_app,
        init_routers,
    )

    application: FastAPI = init_app()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_routers(application)

    return application
