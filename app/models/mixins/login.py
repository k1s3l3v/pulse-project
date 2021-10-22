from sqlalchemy import Column, Enum, String

from ...db import LoginServiceEnum


class ORMLoginMixin:
    login_id = Column(String, nullable=False)
    login_type = Column(Enum(LoginServiceEnum), nullable=False)
