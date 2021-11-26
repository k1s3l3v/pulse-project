from pydantic import Field, PositiveInt

from .base import TrimModel


class ProjectSpecificCriterion(TrimModel):
    project_criterion_id: PositiveInt = Field(..., description='The project criterion unique identifier')
    is_mandatory: bool = Field(..., description='Whether the criterion is mandatory')

    class Config(TrimModel.Config):
        orm_mode = True
