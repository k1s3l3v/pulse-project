from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..dependencies import get_current_user, get_db
from ..models.orms import ProjectCriterionValueORM
from ..services import ProjectCriterionValue, ProjectSpecificCriterion, ProjectStatus
from ..utils import commit_transaction


router = APIRouter(prefix='/project_pulse', tags=['project_pulse'])


@router.get(
    '/{project_id}',
    dependencies=[Depends(get_current_user)],
    response_model=schemas.ProjectPulse,
    responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Not found'},
        500: {'description': 'Internal server error'}
    }
)
async def get_project_pulse_by_id(
        project_id: int = Path(..., description='The identifier of the project to get pulse data', gt=0),
        db: Session = Depends(get_db)
):
    """Get project pulse data by id"""
    await ProjectSpecificCriterion.check_remote_project_existence(project_id)

    status = ProjectStatus.get_by_project_id(db, project_id)
    criteria = ProjectSpecificCriterion.get_list_by_project_id(db, project_id)
    return schemas.ProjectPulse(criteria=criteria, status=status)


@router.put(
    '/{project_id}',
    response_model=schemas.ProjectPulse,
    responses={
        200: {'description': 'Success'},
        400: {'description': 'Bad request'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Not found'},
        500: {'description': 'Internal server error'}
    }
)
async def update_project_pulse_by_id(
        payload: schemas.ProjectPulseUpdate,
        project_id: int = Path(..., description='The identifier of the project to update pulse data', gt=0),
        current_user_id: int = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Update project criterion value by id"""
    if len(payload.__fields_set__) == 2:
        await ProjectSpecificCriterion.check_remote_project_existence(project_id)
    else:
        criterion_value: ProjectCriterionValueORM = ProjectCriterionValue.get_by_id(db, project_id,
                                                                                    payload.project_criterion_id,
                                                                                    payload.date)
        if criterion_value is not None:
            data = payload.dict()
            data['author_id'] = current_user_id
            await ProjectCriterionValue.update_object(db, data, criterion_value)
        else:
            data = payload.dict(exclude_unset=False)
            data['author_id'] = current_user_id
            data['project_id'] = project_id
            await ProjectCriterionValue.create(db, data)
        commit_transaction(db)
    status = ProjectStatus.get_by_project_id(db, project_id)
    criteria = ProjectSpecificCriterion.get_list_by_project_id(db, project_id)
    return schemas.ProjectPulse(criteria=criteria, status=status)
