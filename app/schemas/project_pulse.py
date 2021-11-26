from pydantic import Field
from typing import List

from .base import TrimModel
from .project_specific_criterion import ProjectSpecificCriterion
from .project_status import ProjectStatus


class ProjectPulse(TrimModel):
    status: ProjectStatus = Field(None, description='Common project status')
    criteria: List[ProjectSpecificCriterion] = Field(..., description='List of existing criteria for current project')
