from sqlalchemy import Boolean, Column, ForeignKey, Integer, select
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import relationship

from .base import BaseORM
from ..mixins import DateORMMixin
from .project_criterion import ProjectCriterionORM


def is_mandatory_default(context: DefaultExecutionContext) -> bool:
    if context is None:
        return False
    project_criterion_id = context.get_current_parameters()['project_criterion_id']
    return select(ProjectCriterionORM.is_mandatory) \
        .filter(ProjectCriterionORM.project_criterion_id == project_criterion_id)


class ProjectSpecificCriterionORM(BaseORM, DateORMMixin):
    project_id = Column(Integer, primary_key=True)
    project_criterion_id = Column(ForeignKey('project_criterion.project_criterion_id', ondelete='CASCADE'),
                                  primary_key=True)
    is_mandatory = Column(Boolean, default=is_mandatory_default, nullable=False)

    project_criterion = relationship('ProjectCriterionORM')

    def __repr__(self):
        return f'<project_specific_criterion {self.name}>'
