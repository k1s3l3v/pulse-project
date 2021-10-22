# models

Package for ORMs and mixins for it

Each new ORM must be inherited from `ORMBase` class

It can be
```python
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from .base import ORMBase
from ...db import SomeEnum


class ORMExample1(ORMBase):
    __tablename__ = 'example1'

    example_id = Column(Integer, ORMBase.seq, primary_key=True, server_default=ORMBase.seq.next_value())
    enum = Column(Enum(SomeEnum), nullable=False)
    example3_id = Column(Integer, ForeignKey('example3.example3_id'), nullable=False)
    string = Column(String, default='', nullable=False)
    json = Column(JSON, default={}, nullable=False)
    nullable_string = Column(String)

    created_at = Column(DateTime, default=ORMBase.now, nullable=False)
    updated_at = Column(DateTime, default=ORMBase.now, onupdate=ORMBase.now, nullable=False)

    foreign_key_cascade_delete = relationship('ORMExample2', back_populates='example', cascade='all, delete')

    @property
    def some_property(self) -> bool:
        return True
```

Please, pay attention to the default value for the primary key

Please, pay attention to the nullable fields: you must write `nullable=False` if field value can't be `null`
