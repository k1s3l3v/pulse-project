from sqlalchemy.orm import Session
from typing import Optional

from ..cruds.base import DictStrAny
from ...exceptions import UpdateError
from ...models import NameBaseORM


class NameMixin:
    model = NameBaseORM

    @classmethod
    def get_by_name(cls, db: Session, name: str) -> Optional[model]:
        return db.query(cls.model).filter_by(name=name).first()

    @classmethod
    async def _update_name(cls, db: Session, object_: model, data: DictStrAny) -> model:
        if 'name' in data and (name := data['name']) != object_.name:
            if cls.get_by_name(db, name) is None:
                object_.name = name
            else:
                raise UpdateError(object_,
                                  f"{object_.__tablename__.replace('_', ' ')} with name '{name}' already exists")

        return object_
