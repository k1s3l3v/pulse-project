from sqlalchemy import CheckConstraint, Column, Date, Integer, JSON
from sqlalchemy.ext.mutable import MutableDict, MutableList

from .base import BaseORM
from ..mixins import DateORMMixin


class ProjectStatusORM(BaseORM, DateORMMixin):
    __table_args__ = (
        CheckConstraint('1 <= project_status.project_id', 'ck_project_status_project_id'),
    )

    project_status_id = Column(Integer, BaseORM.seq, primary_key=True, server_default=BaseORM.seq.next_value())
    project_id = Column(Integer, nullable=False, unique=True)
    aggregated_value = Column(Integer, nullable=False)
    latest_updated_at = Column(Date, default=DateORMMixin.date_now, nullable=False)
    latest_updater_id = Column(Integer)
    latest_grades = Column(MutableDict.as_mutable(JSON), default={}, nullable=False)
    latest_log = Column(MutableList.as_mutable(JSON), default=[], nullable=False)

    def __repr__(self):
        return f'<project_status project={self.project_id}>'
