from typing import Literal, Optional

from ..schemas import TrimModel
from ..utils import with_literal_default


class Request(TrimModel):
    type: str


class Response(TrimModel):
    pass


@with_literal_default
class VerifyTokenRequest(Request):
    type: Literal['verify_token']
    token: str


@with_literal_default
class CheckStaffProjectRequest(Request):
    type: Literal['check_staff_project']
    staff_id: int
    project_id: int
    role: Optional[str] = None


class CheckModelResponse(Response):
    model_id: Optional[int] = None


@with_literal_default
class DeleteStaffRequest(Request):
    type: Literal['delete_staff']
    staff_id: int


class DeleteModelResponse(Response):
    success: bool = False


@with_literal_default
class DeleteProjectRequest(Request):
    type: Literal['delete_project']
    project_id: int


@with_literal_default
class DeleteStaffProjectRequest(Request):
    type: Literal['delete_staff_project']
    staff_id: int
    project_id: int
