from sqlalchemy.orm import Session
from typing import Optional

from ...models import NameBaseORM


class NameMixin:
    model = NameBaseORM

    @classmethod
    def get_by_name(cls, db: Session, name: str) -> Optional[NameBaseORM]:
        return db.query(cls.model).filter_by(name=name).first()
