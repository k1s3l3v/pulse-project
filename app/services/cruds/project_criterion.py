from .base import Base, DictStrAny, Session
from ..mixins import NameMixin
from ...exceptions import CreationError
from ...models import ProjectCriterionORM


class ProjectCriterion(Base, NameMixin):
    model = ProjectCriterionORM

    columns_to_update = [ProjectCriterionORM.name, ProjectCriterionORM.is_mandatory,
                         ProjectCriterionORM.normal_threshold, ProjectCriterionORM.max_value]

    simple_columns_to_update = [ProjectCriterionORM.is_mandatory]

    @classmethod
    async def _before_create(cls, db: Session, data: DictStrAny) -> ProjectCriterionORM:
        project_criterion: ProjectCriterionORM = cls.create_object(data)

        db_project_criterion = cls.get_by_name(db, project_criterion.name)
        if db_project_criterion is not None:
            raise CreationError('ProjectCriterion',
                                f"project criterion with name '{project_criterion.name}' already exists")

        if not 1 <= project_criterion.max_value:
            raise CreationError('ProjectCriterion', f"max value must be >= 1, not '{project_criterion.max_value}'")

        if not 1 <= project_criterion.normal_threshold <= project_criterion.max_value:
            raise CreationError('ProjectCriterion',
                                f"normal threshold must be in [1; {project_criterion.max_value}], not "
                                f"'{project_criterion.normal_threshold}'")

        return project_criterion

    @classmethod
    async def _update_complicated_columns(cls, db: Session, project_criterion: ProjectCriterionORM,
                                          data: DictStrAny) -> ProjectCriterionORM:
        if 'name' in data and cls.get_by_name(db, data['name']) is None:
            project_criterion.name = data['name']

        if 'normal_threshold' in data or 'max_value' in data:
            normal_threshold = data.get('normal_threshold', project_criterion.normal_threshold)
            max_value = data.get('max_value', project_criterion.max_value)
            if 1 <= normal_threshold <= max_value:
                project_criterion.normal_threshold = normal_threshold
                project_criterion.max_value = max_value

        return project_criterion
