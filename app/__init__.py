from asyncio import get_running_loop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import admin, celery, db, exceptions, models, mq, routers, services, templates
from .config import settings


app = FastAPI(title='MADO pulse API', description='API for MADO pulse service', version=settings.VERSION,
              openapi_url=f'{settings.URL_PREFIX}/openapi.json',
              swagger_ui_init_oauth={'clientId': settings.ITS_CLIENT_ID},
              docs_url=f'{settings.URL_PREFIX}/docs', redoc_url=f'{settings.URL_PREFIX}/redoc')

app.mount(f'{settings.URL_PREFIX}/static', StaticFiles(directory='app/static'), name='static')


@app.on_event('startup')
async def startup_event():
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


def init_app() -> FastAPI:
    if len(settings.CORS_ORIGINS) > 0:
        app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True,
                           allow_methods=['*'], allow_headers=['*'])
    exceptions.init_app(app)
    routers.init_app(app)
    admin.init_app(app)
    return app
