<<<<<<< HEAD
from sqlalchemy import CheckConstraint, Column, Date, Integer, ForeignKeyConstraint, String
from sqlalchemy.orm import relationship

from .base import BaseORM
from ..mixins import DateORMMixin


class ProjectCriterionValueORM(BaseORM, DateORMMixin):
    __table_args__ = (
        CheckConstraint('1 <= project_criterion_value.value', 'ck_project_criterion_value_value'),
        CheckConstraint('project_criterion_value.author_id IS NULL OR 1 <= project_criterion_value.author_id',
                        'ck_project_criterion_value_author_id'),
        ForeignKeyConstraint(('project_id', 'project_criterion_id'),
                             ('project_specific_criterion.project_id',
                              'project_specific_criterion.project_criterion_id'), ondelete='CASCADE')
    )

    project_id = Column(primary_key=True)
    project_criterion_id = Column(primary_key=True)
    date = Column(Date, primary_key=True)
    value = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    author_id = Column(Integer)

    project_specific_criterion = relationship('ProjectSpecificCriterionORM')

    def __repr__(self):
        return f'<project_criterion_value project={self.project_id}, ' \
               f'{self.project_specific_criterion.project_criterion.name}>'
=======
from sqlalchemy import CheckConstraint, Column, Date, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import BaseORM
from ..mixins import DateORMMixin


class ProjectCriterionValueORM(BaseORM, DateORMMixin):
    __table_args__ = (
        CheckConstraint('1 <= project_criterion_value.value', 'ck_project_criterion_value_value'),
    )

    project_id = Column(Integer, primary_key=True)
    project_criterion_id = Column(ForeignKey('project_criterion.project_criterion_id', ondelete='CASCADE'),
                                  primary_key=True)
    date = Column(Date, primary_key=True)
    value = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    author_id = Column(Integer, nullable=False)

    project_criterion = relationship('ProjectCriterionORM')

    def __repr__(self):
        return f'<project_criterion_value {self.name}>'
>>>>>>> dabb50d7e5639e890a96ccdc69e3f6e42dd98f2d
