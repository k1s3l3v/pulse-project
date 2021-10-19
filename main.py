import uvicorn

from app import init_app, settings


app = init_app()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=settings.PORT, reload=True)
