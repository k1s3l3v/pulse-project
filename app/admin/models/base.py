from sqlalchemy import inspect
from sqlalchemy.orm import Session
from typing import Type

from ...models import BaseORM


class AdminBaseORM(BaseORM):
    __abstract__ = True

    is_public = False

    @classmethod
    def connect_db(cls, session: Session):
        class Query(object):
            def __get__(self, instance: 'AdminBaseORM', owner: Type['AdminBaseORM']):
                return session.query(inspect(owner))

        cls.query = Query()
