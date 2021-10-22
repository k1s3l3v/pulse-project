from fastapi import FastAPI
from fastapi.routing import APIRouter

from . import auth, default
from ..config import settings


def init_app(app: FastAPI):
    router = APIRouter(prefix=settings.URL_PREFIX)
    router.include_router(default.router)
    router.include_router(auth.router)
    app.include_router(router)
