from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..dependencies import get_current_user, get_db
from ..services import ProjectSpecificCriterion, ProjectStatus


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
