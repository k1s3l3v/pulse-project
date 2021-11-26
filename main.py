import uvicorn

from app import get_app, settings


app = get_app()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=settings.PORT, reload=True)
