import json

from asyncio import new_event_loop
from datetime import datetime, timedelta
from functools import lru_cache
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Any, Awaitable, Iterable, Type


def all_in(params: Iterable, data: Iterable) -> bool:
    return all(p in data for p in params)


def any_in(params: Iterable, data: Iterable) -> bool:
    return any(p in data for p in params)


def commit_transaction(db: Session, throw: bool = True):
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        if throw:
            raise e


@lru_cache()
def get_db_initialization_data() -> dict:
    with open('app/db/init.json') as f:
        data = json.load(f)
    return data


def now() -> datetime:
    return datetime.utcnow() + timedelta(hours=3)


def run_asyncio_coroutine(coroutine: Awaitable) -> Any:
    loop = new_event_loop()
    try:
        result = loop.run_until_complete(coroutine)
    finally:
        loop.close()
    return result


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def with_literal_default(cls: Type[BaseModel]):
    from pydantic.fields import ModelField
    from typing import get_args, get_origin, Literal

    for model_field in cls.__fields__.values():
        model_field: ModelField
        if get_origin(model_field.type_) is Literal and model_field.default is None:
            default = get_args(model_field.type_)[0]
            model_field.field_info.default = default
            model_field.default = default
            model_field.required = False
    return cls
