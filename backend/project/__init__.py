from fastapi import FastAPI

from project.wines import wine_router                # new


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(wine_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
