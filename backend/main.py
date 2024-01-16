import uvicorn

from config.app import get_fastapi_app
from config import site_config


app = get_fastapi_app()


if __name__ == "__main__":
    uvicorn.run("main:app", **site_config.model_dump())
