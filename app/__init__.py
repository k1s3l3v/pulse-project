from asyncio import get_running_loop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Optional

from . import admin, celery, db, exceptions, models, mq, redis, routers, services, templates
from .config import settings


_app: Optional[FastAPI] = None


def _init_app() -> FastAPI:
    app = FastAPI(title='MADO pulse API', description='API for MADO pulse service', version=settings.VERSION,
                  openapi_url=f'{settings.URL_PREFIX}/openapi.json',
                  swagger_ui_init_oauth={'clientId': settings.PM_CLIENT_ID},
                  docs_url=f'{settings.URL_PREFIX}/docs', redoc_url=f'{settings.URL_PREFIX}/redoc')
    app.mount(f'{settings.URL_PREFIX}/static', StaticFiles(directory='app/static'), name='static')
    if len(settings.CORS_ORIGINS) > 0:
        app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True,
                           allow_methods=['*'], allow_headers=['*'])
    exceptions.init_app(app)
    routers.init_app(app)
    admin.init_app(app)

    @app.on_event('startup')
    async def startup_event():
        with redis.get_lock('startup:init'):
            admin.init_admin_tables()
            session = db.create_session()
            # Call `init` functions of services
            session.close()
        loop = get_running_loop()
        await mq.Connection().open(loop)
        await mq.staffClient.init(loop)
        await mq.pulseServer.consume()

    @app.on_event('shutdown')
    async def shutdown_event():
        admin.disconnect_db()
        db.disconnect_db()
        await mq.Connection().close()

    return app


def get_app() -> FastAPI:
    global _app

    if _app is None:
        _app = _init_app()
    return _app
