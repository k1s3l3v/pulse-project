from pydantic import Field
from typing import List

from .base import TrimModel
from .project_specific_criterion import ProjectSpecificCriterion
from .project_status import ProjectStatus


class ProjectPulse(TrimModel):
    status: ProjectStatus = Field(None, description='Common project status')
    criteria: List[ProjectSpecificCriterion] = Field(..., description='List of existing criteria for current project')


class ProjectPulseUpdate(TrimModel):
    project_criterion_id: PositiveInt = Field(..., description='The project criterion identifier')
    date: date_ = Field(..., description='Date of pulse update')
    value: PositiveInt = Field(1, description='New pulse value')
    comment: str = Field('', description='Few words about update')
 
