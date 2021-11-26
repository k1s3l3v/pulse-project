from fastapi import FastAPI
from fastapi.routing import APIRouter

from . import default, entity, project_pulse
from ..config import settings


def init_app(app: FastAPI):
    router = APIRouter(prefix=settings.URL_PREFIX)
    router.include_router(default.router)
    router.include_router(entity.router)
    router.include_router(project_pulse.router)
    app.include_router(router)
