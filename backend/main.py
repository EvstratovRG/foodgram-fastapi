import uvicorn

from config import site_config
from config.app import get_fastapi_app

app = get_fastapi_app()


if __name__ == "__main__":
    uvicorn.run("main:app", **site_config.model_dump())
