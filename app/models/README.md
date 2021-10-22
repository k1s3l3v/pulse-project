# models

Package for ORMs and mixins for it

Each new ORM must be inherited from `BaseORM` class

It can be
```python
from sqlalchemy import Column, Enum, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from .base import BaseORM
from ..mixins import DateORMMixin
from ...db import SomeEnum


class Example1ORM(BaseORM, DateORMMixin):
    example1_id = Column(Integer, BaseORM.seq, primary_key=True, server_default=BaseORM.seq.next_value())
    enum = Column(Enum(SomeEnum), nullable=False)
    example2_id = Column(Integer, ForeignKey('example2.example2_id'), nullable=False)
    string = Column(String, default='', nullable=False)
    json = Column(JSON, default={}, nullable=False)
    nullable_string = Column(String)

    example2 = relationship('Example2ORM')

    @property
    def some_property(self) -> bool:
        return True
```

Please, pay attention to the default value for the primary key

Please, pay attention to the nullable fields: you must write `nullable=False` if field value can't be `null`
