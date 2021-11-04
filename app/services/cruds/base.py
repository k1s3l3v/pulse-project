from sqlalchemy import Column
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional, Union

from ...exceptions import DeletionError, ModelNotFoundError
from ...models import BaseORM
from ...models.orms.base import PKType
from ...utils import any_in, commit_transaction


DictStrAny = Dict[str, Any]


class Base:
    model = BaseORM

    columns_to_update: List[Column] = []
    simple_columns_to_update: List[Column] = []
    editable_pk_columns: List[Column] = []

    @classmethod
    def get_columns(cls) -> List[Column]:
        return list(cls.model.__table__.columns.values())

    @classmethod
    def get_by_id(cls, db: Session, *args: PKType) -> BaseORM:
        filters = {pk_name: pk_value for pk_name, pk_value in zip(cls.model.get_pk_names(), args)}
        return db.query(cls.model).filter_by(**filters).first()

    @classmethod
    def get_list(cls, db: Session, skip: int = 0, limit: Optional[int] = None) -> List[BaseORM]:
        query = db.query(cls.model).order_by(*cls.model.get_pk_columns()).offset(skip)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    @classmethod
    def get_count(cls, db: Session) -> int:
        return db.query(cls.model).count()

    @classmethod
    def commit(cls, db: Session):
        commit_transaction(db)

    @classmethod
    def refresh(cls, db: Session, objects: Union[List[BaseORM], BaseORM]):
        if isinstance(objects, list):
            for object_ in objects:
                db.refresh(object_)
        else:
            db.refresh(objects)

    @classmethod
    def _update_columns(cls, object_: BaseORM, data: DictStrAny, columns: List[Column]) -> BaseORM:
        for column in columns:
            if column.name in data and ((data[column.name] is None and column.nullable)
                                        or data[column.name] is not None):
                setattr(object_, column.name, data[column.name])
        return object_

    @classmethod
    async def _before_create(cls, db: Session, object_: BaseORM):
        pass

    @classmethod
    async def create(cls, db: Session, data: DictStrAny) -> BaseORM:
        object_ = cls.model(**data)
        await cls._before_create(db, object_)
        db.add(object_)
        return object_

    @classmethod
    def check_existence(cls, db: Session, *args: PKType) -> BaseORM:
        object_ = cls.get_by_id(db, *args)
        if object_ is None:
            raise ModelNotFoundError(cls.model.__name__[:-3], *args)
        return object_

    @classmethod
    async def _update_complicated_columns(cls, db: Session, object_: BaseORM, data: DictStrAny) -> BaseORM:
        return object_

    @classmethod
    def _need_to_update(cls, data: DictStrAny) -> bool:
        return any_in([column.key for column in cls.columns_to_update], data)

    @classmethod
    async def update(cls, db: Session, data: DictStrAny, *args: PKType) -> BaseORM:
        object_ = cls.check_existence(db, *args)
        for pk_column in filter(lambda c: c not in cls.editable_pk_columns, cls.model.get_pk_columns()):
            data.pop(pk_column.key, None)
        if not cls._need_to_update(data):
            return object_
        object_ = cls._update_columns(object_, data, cls.simple_columns_to_update)
        object_ = await cls._update_complicated_columns(db, object_, data)
        db.add(object_)
        return object_

    @classmethod
    async def _before_delete(cls, object_: BaseORM):
        pass

    @classmethod
    async def delete(cls, db: Session, *args: PKType) -> BaseORM:
        object_ = cls.check_existence(db, *args)
        if object_.can_delete:
            await cls._before_delete(object_)
            db.delete(object_)
        else:
            raise DeletionError(cls.model.__name__[:-3], *args)
        return object_

    @classmethod
    def init(cls, db: Session):
        pass
