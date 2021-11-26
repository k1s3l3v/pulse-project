from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
from typing import Union

from ..models import BaseORM


class ExceptionWithMessage(Exception):
    def __init__(self, message: str):
        super(ExceptionWithMessage, self).__init__(message)
        self.message = message


class CreationError(ExceptionWithMessage):
    def __init__(self, model: str, message: str):
        message_ = f"{model} can't be created: {message}"
        super(CreationError, self).__init__(message_)


class ModelNotFoundError(ExceptionWithMessage):
    def __init__(self, model: str, *args: Union[int, str]):
        message = f'{model} ({", ".join(map(str, args))}) not found'
        super(ModelNotFoundError, self).__init__(message)


class UpdateError(ExceptionWithMessage):
    def __init__(self, object_: BaseORM, message: str):
        message_ = f"{object_} can't be updated: {message}"
        super(UpdateError, self).__init__(message_)


class DeletionError(ExceptionWithMessage):
    def __init__(self, model: str, *args: int):
        message = f"{model} ({', '.join(map(str, args))}) can't be deleted"
        super(DeletionError, self).__init__(message)


class ServiceDeliveryError(ExceptionWithMessage):
    pass


class ServiceResponseError(ExceptionWithMessage):
    pass


def init_app(app: FastAPI):
    @app.exception_handler(CreationError)
    def handle_creation_error(request: Request, exc: CreationError):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': exc.message})

    @app.exception_handler(ModelNotFoundError)
    def handle_model_not_found_error(request: Request, exc: ModelNotFoundError):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'detail': exc.message})

    @app.exception_handler(UpdateError)
    def handle_update_error(request: Request, exc: UpdateError):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': exc.message})

    @app.exception_handler(DeletionError)
    def handle_deletion_error(request: Request, exc: DeletionError):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={'detail': exc.message})

    @app.exception_handler(ServiceDeliveryError)
    def handle_deletion_error(request: Request, exc: ServiceDeliveryError):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': exc.message})

    @app.exception_handler(ServiceResponseError)
    def handle_deletion_error(request: Request, exc: ServiceResponseError):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'detail': exc.message})

    @app.exception_handler(OperationalError)
    def handle_operational_error(request: Request, exc: OperationalError):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'detail': 'Unable to establish a connection to the database'})
