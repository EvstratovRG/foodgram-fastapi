import uvicorn

from config.app import get_fastapi_app
from config import site_config

app = get_fastapi_app()


if __name__ == "__main__":
    uvicorn.run("main:app", **site_config)

# app = FastAPI(
#     title='Foodgram'
# )

# app.include_router(get_routers())


# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
