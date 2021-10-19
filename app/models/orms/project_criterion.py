from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint

from .base import BaseORM
from ..mixins import DateORMMixin


class ProjectCriterion(BaseORM, DateORMMixin):
    __table_args__ = (
        CheckConstraint('1 <= project_criterion.normal_threshold AND project_criterion.normal_threshold <= max_value', 'ck_project_criterion_normal_threshold'),
        CheckConstraint('1 <= project_criterion.max_value', 'ck_project_criterion_max_value')
    )

    project_criterion_id = Column(Integer, BaseORM.seq, primary_key=True)
    name = Column(String, uniqie=True, nullable=False)
    is_mandatory = Column(Boolean, default=False, nullable=False)
    max_value = Column(Integer, default=5, nullable=False)
    normal_threshold = Column(Integer, default=3, nullable=False)

    def __repr__(self):
        return f'<project_criterion {self.name}>'


