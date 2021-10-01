from datetime import datetime, timedelta
from sqlalchemy import Column, Sequence
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class ORMBase:
    __abstract__ = True

    seq = Sequence('mado_seq')

    @property
    def can_delete(self) -> bool:
        return True

    @classmethod
    def id_column(cls) -> Column:
        return cls.__table__.primary_key.columns[0]

    @classmethod
    def now(cls) -> datetime:
        return datetime.utcnow() + timedelta(hours=3)
