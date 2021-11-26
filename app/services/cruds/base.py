from sqlalchemy import Column
from sqlalchemy.orm import Session
from typing import Any, Dict, Iterable, List, Optional, Set, Union

from ...exceptions import DeletionError, ModelNotFoundError
from ...models import BaseORM
from ...models.orms.base import PKType
from ...utils import commit_transaction


DictStrAny = Dict[str, Any]


class Base:
    model = BaseORM

    columns_to_update: Set[Column] = set()
    simple_columns_to_update: Set[Column] = set()
    editable_pk_columns: Set[Column] = set()

    @classmethod
    def get_columns(cls) -> List[Column]:
        return list(cls.model.__table__.columns.values())

    @classmethod
    def get_by_id(cls, db: Session, *args: PKType) -> model:
        filters = {pk_name: pk_value for pk_name, pk_value in zip(cls.model.get_pk_names(), args)}
        return db.query(cls.model).filter_by(**filters).first()

    @classmethod
    def get_list(cls, db: Session, skip: int = 0, limit: Optional[int] = None) -> List[model]:
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
    def refresh(cls, db: Session, objects: Union[List[model], model]):
        if isinstance(objects, list):
            for object_ in objects:
                db.refresh(object_)
        else:
            db.refresh(objects)

    @classmethod
    def _update_columns(cls, object_: model, data: DictStrAny, columns: Iterable[Column]) -> model:
        for column in columns:
            if column.name in data and data[column.name] != getattr(object_, column.name) \
                    and ((data[column.name] is None and column.nullable) or data[column.name] is not None):
                setattr(object_, column.name, data[column.name])
        return object_

    @classmethod
    def create_object(cls, data: DictStrAny) -> model:
        return cls.model(**data)

    @classmethod
    async def _before_create(cls, db: Session, data: DictStrAny) -> model:
        return cls.model(**data)

    @classmethod
    async def _after_create(cls, db: Session, object_: model):
        pass

    @classmethod
    async def create(cls, db: Session, data: DictStrAny) -> model:
        object_ = await cls._before_create(db, data)
        db.add(object_)
        await cls._after_create(db, object_)
        return object_

    @classmethod
    def check_existence(cls, db: Session, *args: PKType) -> model:
        object_ = cls.get_by_id(db, *args)
        if object_ is None:
            raise ModelNotFoundError(cls.model.__name__[:-3], *args)
        return object_

    @classmethod
    async def _update_complicated_columns(cls, db: Session, object_: model, data: DictStrAny) -> model:
        return object_

    @classmethod
    def _need_to_update(cls, data: DictStrAny, object_: model) -> bool:
        return any(column.key in data
                   and (column not in cls.simple_columns_to_update or data[column.key] != getattr(object_, column.key))
                   for column in cls.columns_to_update)

    @classmethod
    def is_object_modified(cls, db: Session, object_: model, pure: bool = False) -> bool:
        return db.is_modified(object_) if pure else object_ in db.dirty

    @classmethod
    async def _after_update(cls, db: Session, object_: model):
        pass

    @classmethod
    async def update_object(cls, db: Session, data: DictStrAny, object_: model) -> model:
        for pk_column in filter(lambda c: c not in cls.editable_pk_columns, cls.model.get_pk_columns()):
            data.pop(pk_column.key, None)
        if not cls._need_to_update(data, object_):
            return object_
        object_ = cls._update_columns(object_, data, cls.simple_columns_to_update)
        object_ = await cls._update_complicated_columns(db, object_, data)
        if cls.is_object_modified(db, object_):
            db.add(object_)
            await cls._after_update(db, object_)
        return object_

    @classmethod
    async def update(cls, db: Session, data: DictStrAny, *args: PKType) -> model:
        object_ = cls.check_existence(db, *args)
        return await cls.update_object(db, data, object_)

    @classmethod
    async def _before_delete(cls, object_: model):
        pass

    @classmethod
    async def delete_object(cls, db: Session, object_: model) -> model:
        if object_.can_delete:
            await cls._before_delete(object_)
            db.delete(object_)
        else:
            raise DeletionError(cls.model.__name__[:-3], *object_.get_pk_values())
        return object_

    @classmethod
    async def delete(cls, db: Session, *args: PKType) -> model:
        object_ = cls.check_existence(db, *args)
        return await cls.delete_object(db, object_)

    @classmethod
    def init(cls, db: Session):
        pass
