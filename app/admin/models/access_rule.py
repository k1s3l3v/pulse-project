from sqlalchemy import Column, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from .base import AdminBaseORM
from ...models import DateORMMixin


class AdminAccessRuleORM(AdminBaseORM, DateORMMixin):
    id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey('admin_role.id', ondelete='CASCADE'), nullable=False, unique=True)
    tables = Column(JSON, nullable=False)

    role = relationship('AdminRoleORM')
