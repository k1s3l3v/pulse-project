from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from typing import Type

from .db import get_db
from ..config import settings
from ..models import ORMBase, ORMLoginMixin
from ..oauth2 import BaseOAuth2, get_service as get_service_, ITSOAuth2, validate_service


apiKey_scheme = APIKeyHeader(name='authorization',
                             description='The authorization token with service in format service.token',
                             auto_error=False)


oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl=ITSOAuth2.CODE_URL, tokenUrl=ITSOAuth2.TOKEN_URL,
                                              refreshUrl=ITSOAuth2.TOKEN_URL, auto_error=False)


def _get_api_key(key: str = Depends(apiKey_scheme)) -> str:
    if key is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Access token required')
    return key.split(' ')[-1]


def get_api_key_service(key: str = Depends(_get_api_key)) -> Type[BaseOAuth2]:
    service_name = key.split('.')[0]
    if not validate_service(service_name):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid service supplied')
    return get_service_(service_name)


def get_api_key_access_token(key: str = Depends(_get_api_key)) -> str:
    service_name = key.split('.')[0]
    return key[len(service_name) + 1:]


def get_api_key_current_user(service: Type[BaseOAuth2] = Depends(get_api_key_service),
                             access_token: str = Depends(get_api_key_access_token),
                             db: Session = Depends(get_db)) -> Type[ORMBase, ORMLoginMixin]:
    validation_data = service.validate_token(access_token)
    return service.get_user_by_id(db, service.get_id_from_info(validation_data))


def get_oauth2_current_user(access_token: str = Depends(oauth2_scheme),
                            db: Session = Depends(get_db)) -> Type[ORMBase, ORMLoginMixin]:
    validation_data = ITSOAuth2.validate_token(access_token)
    return ITSOAuth2.get_user_by_id(db, ITSOAuth2.get_id_from_info(validation_data))


if settings.USE_OAUTH2_AUTHORIZATION:
    get_access_token = oauth2_scheme
    get_current_user = get_oauth2_current_user

    def get_service():
        return ITSOAuth2
else:
    get_access_token = get_api_key_access_token
    get_current_user = get_api_key_current_user
    get_service = get_api_key_service
