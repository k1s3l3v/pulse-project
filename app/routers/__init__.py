from fastapi import FastAPI
from fastapi.routing import APIRouter

from . import default
from ..config import settings


def init_app(app: FastAPI):
    router = APIRouter(prefix=settings.URL_PREFIX)
    router.include_router(default.router)
    app.include_router(router)
