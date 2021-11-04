from datetime import date, datetime
from sqlalchemy import Column, DateTime

from ...utils import now


class DateORMMixin:
    created_at = Column(DateTime, default=now, nullable=False)
    updated_at = Column(DateTime, default=now, onupdate=now, nullable=False)

    @classmethod
    def now(cls) -> datetime:
        return now()

    @classmethod
    def date_now(cls) -> date:
        return now().date()
