from pydantic import Field, PositiveInt

from .base import TrimModel


class ProjectCriterion(TrimModel):
    project_criterion_id: PositiveInt = Field(..., description='The project criterion unique identifier')
    name: str = Field(..., description='The project criterion name')
    is_mandatory: bool = Field(..., description='Whether the criterion is mandatory')
    max_value: PositiveInt = Field(..., description='The project criterion max value')
    normal_threshold: PositiveInt = Field(..., description='The lowest permissible value for current project criterion')

    class Config(TrimModel.Config):
        orm_mode = True
