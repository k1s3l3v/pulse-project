from flask_security import RoleMixin
from sqlalchemy import Column, Integer, String

from .base import AdminBaseORM
from ...models import DateORMMixin


class AdminRoleORM(AdminBaseORM, RoleMixin, DateORMMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, unique=True)
    description = Column(String(255))

    def __repr__(self):
        return f'<admin_role {self.name}>'
