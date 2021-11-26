from pydantic import ValidationError

from .base import Base, DictStrAny, Session
from ...exceptions import CreationError, ModelNotFoundError, ServiceDeliveryError, ServiceResponseError, UpdateError
from ...models import ProjectCriterionValueORM, ProjectSpecificCriterionORM
from ...mq import CheckModelResponse, CheckStaffProjectRequest, DeliveryError, staffClient


class ProjectCriterionValue(Base):
    model = ProjectCriterionValueORM

    columns_to_update = {ProjectCriterionValueORM.value, ProjectCriterionValueORM.comment,
                         ProjectCriterionValueORM.author_id}

    simple_columns_to_update = {ProjectCriterionValueORM.comment}

    @classmethod
    async def check_remote_author_project_existence(cls, author_id: int, project_id: int):
        try:
            body = CheckStaffProjectRequest(project_id=project_id, staff_id=author_id)
            response = await staffClient.call(body, CheckModelResponse)
        except DeliveryError:
            raise ServiceDeliveryError("Project criterion value can't be created due to troubles with services "
                                       "connection")
        except ValidationError:
            raise ServiceResponseError("Project criterion value can't be created due to service response "
                                       "misunderstanding")
        if response.model_id is None:
            raise ModelNotFoundError('StaffProjectRole', author_id, project_id)

    @classmethod
    async def _before_create(cls, db: Session, data: DictStrAny) -> ProjectCriterionValueORM:
        from .project_specific_criterion import ProjectSpecificCriterion

        project_criterion_value: ProjectCriterionValueORM = cls.create_object(data)

        if project_criterion_value.project_criterion is None \
                and project_criterion_value.project_criterion_id is not None:
            project_specific_criterion: ProjectSpecificCriterionORM = \
                ProjectSpecificCriterion.check_existence(db, project_criterion_value.project_id,
                                                         project_criterion_value.project_criterion_id)
        elif project_criterion_value.project_criterion is not None:
            project_specific_criterion: ProjectSpecificCriterionORM = \
                ProjectSpecificCriterion.check_existence(db, project_criterion_value.project_id,
                                                         project_criterion_value.project_criterion.project_criterion_id)
        else:
            raise CreationError('ProjectCriterionValue', 'Project criterion value must have project criterion')

        db_project_criterion_value = cls.get_by_id(db, project_specific_criterion.project_id,
                                                   project_specific_criterion.project_criterion_id,
                                                   project_criterion_value.date)
        if db_project_criterion_value is not None:
            raise CreationError('ProjectCriterionValue',
                                f"Project criterion value with project id '{project_specific_criterion.project_id}', "
                                f"project criterion id '{project_specific_criterion.project_criterion_id}' and date "
                                f"'{project_criterion_value.date}' already exists")

        max_value = project_specific_criterion.project_criterion.max_value
        if not 1 <= project_criterion_value.value <= max_value:
            raise CreationError('ProjectCriterionValue',
                                f"value must be in [1; {max_value}], not '{project_criterion_value.value}'")

        await cls.check_remote_author_project_existence(project_criterion_value.author_id,
                                                        project_criterion_value.project_id)

        return project_criterion_value

    @classmethod
    async def _after_create(cls, db: Session, project_criterion_value: ProjectCriterionValueORM):
        from .project_status import ProjectStatus

        if project_criterion_value.project_criterion_id is None:
            project_criterion_value.project_criterion_id = \
                project_criterion_value.project_criterion.project_criterion_id
        await ProjectStatus.update_status(db, project_criterion_value)

    @classmethod
    async def update_remote_author_relation(cls, project_criterion_value: ProjectCriterionValueORM,
                                            data: DictStrAny) -> ProjectCriterionValueORM:
        if 'author_id' in data and (author_id := data['author_id']) != project_criterion_value.author_id:
            try:
                body = CheckStaffProjectRequest(project_id=project_criterion_value.project_id, staff_id=author_id)
                response = await staffClient.call(body, CheckModelResponse)
            except DeliveryError:
                raise ServiceDeliveryError("Project criterion value can't be updated due to troubles with services "
                                           "connection")
            except ValidationError:
                raise ServiceResponseError("Project criterion value can't be updated due to service response "
                                           "misunderstanding")
            if response.model_id is not None:
                project_criterion_value.author_id = author_id
            else:
                raise ModelNotFoundError('StaffProjectRole', author_id, project_criterion_value.project_id)

        return project_criterion_value

    @classmethod
    async def _update_complicated_columns(cls, db: Session, project_criterion_value: ProjectCriterionValueORM,
                                          data: DictStrAny) -> ProjectCriterionValueORM:
        max_value = project_criterion_value.project_criterion.max_value
        if 'value' in data and (value := data['value']) != project_criterion_value.value:
            if 1 <= value <= max_value:
                project_criterion_value.value = value
            else:
                raise UpdateError(project_criterion_value, f"value must be in [1; {max_value}], not '{value}'")

        project_criterion_value = await cls.update_remote_author_relation(project_criterion_value, data)

        return project_criterion_value

    @classmethod
    async def _after_update(cls, db: Session, project_criterion_value: ProjectCriterionValueORM):
        from .project_status import ProjectStatus

        await ProjectStatus.update_status(db, project_criterion_value)
