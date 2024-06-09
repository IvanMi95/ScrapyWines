from fastapi import FastAPI

from project.celery_utils import create_celery
from project.wines import wine_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.celery_app = create_celery()

    app.include_router(wine_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}
    return app
