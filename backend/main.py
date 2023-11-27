import uvicorn

from backend.config.app import get_fastapi_app
from backend.config import site_config

app = get_fastapi_app()


if __name__ == "__main__":
    uvicorn.run("main:app", **site_config)
