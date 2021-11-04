from .base import BaseORM
from ..mixins import NameORMMixin


class NameBaseORM(BaseORM, NameORMMixin):
    __abstract__ = True
