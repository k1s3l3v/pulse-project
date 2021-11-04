from sqlalchemy import Column, String


class NameORMMixin:
    name = Column(String, nullable=False, unique=True)
