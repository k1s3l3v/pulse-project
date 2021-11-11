from pydantic import ValidationError

from .base import Base, DictStrAny, Session
from ...exceptions import CreationError, ModelNotFoundError, ServiceDeliveryError, ServiceResponseError
from ...models import ProjectSpecificCriterionORM
from ...mq import CheckModelResponse, CheckProjectRequest, DeliveryError, staffClient


class ProjectSpecificCriterion(Base):
    model = ProjectSpecificCriterionORM

    columns_to_update = [ProjectSpecificCriterionORM.is_mandatory]

    simple_columns_to_update = [ProjectSpecificCriterionORM.is_mandatory]

    @classmethod
    async def check_remote_project_existence(cls, project_id: int):
        try:
            body = CheckProjectRequest(project_id=project_id)
            response = await staffClient.call(body, CheckModelResponse)
        except DeliveryError:
            raise ServiceDeliveryError("Project specific criterion can't be created due to troubles with services "
                                       "connection")
        except ValidationError:
            raise ServiceResponseError("Project specific criterion can't be created due to service response "
                                       "misunderstanding")
        if response.model_id is None:
            raise ModelNotFoundError('Project', project_id)

    @classmethod
    async def _before_create(cls, db: Session, data: DictStrAny) -> ProjectSpecificCriterionORM:
        project_specific_criterion: ProjectSpecificCriterionORM = cls.create_object(data)

        db_project_specific_criterion = cls.get_by_id(db, project_specific_criterion.project_id,
                                                      project_specific_criterion.project_criterion.project_criterion_id)
        if db_project_specific_criterion is not None:
            raise CreationError('ProjectSpecificCriterion',
                                f"relation between '{project_specific_criterion.project_id}' and "
                                f"'{project_specific_criterion.project_criterion.project_criterion_id}' already exists")

        await cls.check_remote_project_existence(project_specific_criterion.project_id)

        return project_specific_criterion
