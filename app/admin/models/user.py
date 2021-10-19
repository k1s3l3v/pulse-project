from flask_security import UserMixin
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import AdminBaseORM
from ...models import DateORMMixin


class AdminUserORM(AdminBaseORM, UserMixin, DateORMMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    active = Column(Boolean, default=False, nullable=False)

    roles = relationship('AdminRoleORM', secondary='admin_user_role')
