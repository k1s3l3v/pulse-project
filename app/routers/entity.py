from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..dependencies import get_current_user, get_db
from ..services import ProjectCriterion


router = APIRouter(prefix='/entity', tags=['entity'])


@router.get(
    '/',
    dependencies=[Depends(get_current_user)],
    response_model=schemas.Entities,
    response_model_exclude_unset=True,
    responses={
        200: {'description': 'Success'},
        401: {'description': 'Unauthorized'}
    }
)
def get_entities(
        project_criteria: bool = Query(False, description='Is it needed to get the project criteria'),
        db: Session = Depends(get_db)
):
    """Get entities"""
    result = schemas.Entities()
    if project_criteria:
        result.project_criteria = ProjectCriterion.get_list(db)

    return result
