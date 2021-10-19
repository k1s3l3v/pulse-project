from sqlalchemy.exc import SQLAlchemyError

from .schemas import DeleteModelResponse, DeleteProjectRequest, DeleteStaffRequest, DeleteStaffProjectRequest
from ..db import create_session
from ..exceptions import DeletionError, ModelNotFoundError
from ..utils import commit_transaction


def delete_project(payload: DeleteProjectRequest) -> DeleteModelResponse:
    session = create_session()
    try:
        project_id = payload.project_id
        # Delete all rows with current project_id
        commit_transaction(session)
        return DeleteModelResponse(success=True)
    except (SQLAlchemyError, DeletionError):
        return DeleteModelResponse()
    finally:
        session.close()
