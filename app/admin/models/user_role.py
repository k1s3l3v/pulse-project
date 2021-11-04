from sqlalchemy import Column, ForeignKey

from .base import AdminBaseORM
from ...models import DateORMMixin


class AdminUserRoleORM(AdminBaseORM, DateORMMixin):
    user_id = Column(ForeignKey('admin_user.id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(ForeignKey('admin_role.id', ondelete='CASCADE'), primary_key=True)
