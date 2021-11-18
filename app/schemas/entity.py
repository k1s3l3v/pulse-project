from pydantic import Field
from typing import List

from .base import TrimModel
from .project_criterion import ProjectCriterion


class Entities(TrimModel):
    project_criteria: List[ProjectCriterion] = Field(None, description='The project criteria')
