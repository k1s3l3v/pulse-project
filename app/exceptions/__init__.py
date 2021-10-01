from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class ExceptionWithMessage(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ModelNotFoundError(ExceptionWithMessage):
    pass


class DeletionError(ExceptionWithMessage):
    pass


def init_app(app: FastAPI):
    @app.exception_handler(ModelNotFoundError)
    def unicorn_exception_handler(request: Request, exc: ModelNotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': exc.message})

    @app.exception_handler(DeletionError)
    def unicorn_exception_handler(request: Request, exc: DeletionError):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': exc.message})
