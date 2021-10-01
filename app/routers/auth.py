from fastapi import Depends, status, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from sqlalchemy.orm import Session

from .. import schemas
from ..db import LoginServiceEnum
from ..dependencies import get_db, get_trimmed_query
from ..oauth2 import get_service
# from ..services import Staff


router = APIRouter(prefix='/auth', tags=['auth'])


@router.get(
    '/code',
    response_class=RedirectResponse,
    response_description='Redirect to page with code',
    status_code=303
)
def get_code_url(
        service: LoginServiceEnum = Depends(get_trimmed_query('service', LoginServiceEnum.ITS,
                                                              description='The login service')),
        redirect_uri: str = Depends(get_trimmed_query('redirect_uri', ..., description='The redirect uri'))
):
    """Redirect to page with code"""
    return RedirectResponse(get_service(service.value).get_code_url(redirect_uri), status.HTTP_303_SEE_OTHER)


@router.post(
    '/token',
    response_model=schemas.AccessToken,
    responses={
        200: {'description': 'Success'},
        501: {'description': 'Not implemented'}
    }
)
def get_token(
        service: LoginServiceEnum = Query(LoginServiceEnum.ITS, description='The login service'),
        grant_type: schemas.AuthGrantType = Query(schemas.AuthGrantType.authorization_code,
                                                  description='The grant type'),
        code: str = Depends(get_trimmed_query('code', None, description='The authorization code')),
        redirect_uri: str = Depends(get_trimmed_query('redirect_uri', None, description='The redirect uri')),
        refresh_token: str = Depends(get_trimmed_query('refresh_token', None, description='The refresh token')),
        db: Session = Depends(get_db)
):
    """Get access token"""
    service_name = service.value
    service = get_service(service_name)

    if grant_type == schemas.AuthGrantType.authorization_code:
        errors = []
        if code is None:
            errors.append(ErrorWrapper(MissingError(), ['query', 'code']))
        if redirect_uri is None:
            errors.append(ErrorWrapper(MissingError(), ['query', 'redirect_uri']))
        if len(errors) > 0:
            raise RequestValidationError(errors)
        token_response, staff_info = service.get_access_token(code, redirect_uri)
    else:
        if refresh_token is None:
            raise RequestValidationError([ErrorWrapper(MissingError(), ['query', 'refresh_token'])])
        token_response, staff_info = service.get_refresh_token(refresh_token)

    # staff = Staff.get_staff_by_login(db, service.get_id_from_info(staff_info), service_name)
    #
    # if staff is None:
    #     data = service.transform_info(staff_info)
    #     staff = Staff.create(db, data)

    access_token, refresh_token, expires_in = token_response
    # return schemas.AccessToken(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in,
    #                            staff=staff)
    return schemas.AccessToken(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in)
