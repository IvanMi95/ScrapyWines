from fastapi import APIRouter

wine_router = APIRouter(
    prefix="/wines",
)

from . import api  # noqa
