from fastapi import FastAPI


def get_fastapi_app() -> FastAPI:
    from config.initializers import (
        init_app,
        init_routers,
    )

    application: FastAPI = init_app()

    init_routers(application)

    return application
