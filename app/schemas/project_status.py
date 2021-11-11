from datetime import date as date_
from pydantic import ConstrainedInt, Field, PositiveInt
from typing import Dict, List

from .base import TrimModel


class CriterionValue(ConstrainedInt):
    ge = 1


class ProjectStatusLatestGrade(TrimModel):
    project_criterion_id: PositiveInt = Field(..., description='The project criterion unique identifier')
    date: date_ = Field(..., description='Date, when grade was created')
    value: CriterionValue = Field(..., description='Last grade project criterion value')
    comment: str = Field(..., description='Comment about last grade addition')
    author_id: PositiveInt = Field(None, description='Unique identifier of person who added grade')

    class Config(TrimModel.Config):
        orm_mode = True


class ProjectStatusLatestLogRecord(TrimModel):
    project_criterion_id: PositiveInt = Field(..., description='The project criterion unique identifier')
    date: date_ = Field(..., description='Date, when grade was created')
    old_value: CriterionValue = Field(None, description='Previous grade project criterion value')
    new_value: CriterionValue = Field(..., description='New grade project criterion value')
    comment: str = Field(..., description='Comment about last grade addition')
    author_id: PositiveInt = Field(None, description='Unique identifier of person who added last log')

    class Config(TrimModel.Config):
        orm_mode = True


class ProjectStatusCreate(TrimModel):
    project_id: PositiveInt = Field(..., description='Unique project identifier')
    aggregated_value: CriterionValue = Field(..., description='Final value')
    latest_updated_at: date_ = Field(..., description='Last updated date')
    latest_updater_id: PositiveInt = Field(None, description='Unique identifier of person who introduced last changes')
    latest_grades: Dict[str, ProjectStatusLatestGrade] = Field(..., description='Last committed grades')
    latest_log: List[ProjectStatusLatestLogRecord] = Field(..., description='Last committed logs')
