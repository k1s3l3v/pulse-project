<<<<<<< HEAD
from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, select
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import relationship

from .base import BaseORM
from .project_criterion import ProjectCriterionORM
from ..mixins import DateORMMixin


def is_mandatory_default(context: DefaultExecutionContext) -> bool:
    if context is None:
        return False
    project_criterion_id = context.get_current_parameters()['project_criterion_id']
    query = select(ProjectCriterionORM.is_mandatory) \
        .filter(ProjectCriterionORM.project_criterion_id == project_criterion_id)
    result = context.connection.execute(query)
    row = result.fetchone()
    return row['is_mandatory']


class ProjectSpecificCriterionORM(BaseORM, DateORMMixin):
    __table_args__ = (
        CheckConstraint('1 <= project_specific_criterion.project_id', 'ck_project_specific_criterion_project_id'),
    )

    project_id = Column(Integer, primary_key=True)
    project_criterion_id = Column(ForeignKey('project_criterion.project_criterion_id', ondelete='CASCADE'),
                                  primary_key=True)
    is_mandatory = Column(Boolean, default=is_mandatory_default, nullable=False)

    project_criterion = relationship(ProjectCriterionORM)

    def __repr__(self):
        return f'<project_specific_criterion project={self.project_id}, {self.project_criterion.name}>'
=======
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
>>>>>>> dabb50d7e5639e890a96ccdc69e3f6e42dd98f2d
