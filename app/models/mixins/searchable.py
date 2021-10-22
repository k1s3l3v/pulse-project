from sqlalchemy import Column
from typing import List


class ORMSearchableMixin:
    __tablename__: str

    __searchable__: List[Column] = []
