import re

from datetime import date
from sqlalchemy import Column, inspect, Sequence
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Iterator, Optional, Tuple, Union


def camel_to_snake_case(name):
    name = re.sub(r'((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', name)
    return name.lower().lstrip('_')


PKType = Union[int, date]


@as_declarative()
class BaseORM:
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> Optional[str]:
        return camel_to_snake_case(cls.__name__[:-3])

    seq = Sequence('mado_seq')

    is_public = True

    def __init__(self, **kwargs):
        columns = self.__table__.columns
        columns_names = columns.keys()
        for column, value in kwargs.items():
            if column in columns_names and ((value is None and columns[column].nullable) or value is not None):
                setattr(self, column, value)

    def __repr__(self):
        identity = inspect(self).identity
        pk = f'(transient {id(self)})' if identity is None else ', '.join(str(value) for value in identity)
        return f'<{self.__tablename__} {pk}>'

    @property
    def can_delete(self) -> bool:
        return True

    @classmethod
    def get_pk_columns(cls) -> Tuple[Column]:
        return inspect(cls).primary_key

    @classmethod
    def get_pk_names(cls) -> Tuple[str]:
        names: Iterator[str] = (column.name for column in inspect(cls).primary_key)
        return tuple(names)

    def get_pk_values(self) -> Tuple[PKType]:
        values: Iterator[PKType] = (identity for identity in inspect(self).identity)
        return tuple(values)
