import uvicorn
from fastapi import FastAPI

from config.routes import get_routers


app = FastAPI(
    title='Foodgram'
)

app.include_router(get_routers())


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
