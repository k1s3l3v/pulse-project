from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2AuthorizationCodeBearer
from pydantic import ValidationError

from ..config import settings
from ..exceptions import ServiceDeliveryError, ServiceResponseError
from ..mq import CheckModelResponse, DeliveryError, staffClient, VerifyTokenRequest


apiKey_scheme = APIKeyHeader(name='authorization',
                             description='The authorization token with service in format service.token',
                             auto_error=False)


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl='https://keycloak.itsociety.su/auth/realms/its/protocol/openid-connect/auth',
    tokenUrl='https://keycloak.itsociety.su/auth/realms/its/protocol/openid-connect/token',
    refreshUrl='https://keycloak.itsociety.su/auth/realms/its/protocol/openid-connect/token', auto_error=False)


async def _verify_token(access_token: str) -> int:
    try:
        body = VerifyTokenRequest(token=access_token)
        response = await staffClient.call(body, CheckModelResponse)
    except DeliveryError:
        raise ServiceDeliveryError(f"Token {access_token} can't be verified due to troubles with services connection")
    except ValidationError:
        raise ServiceResponseError(f"Token {access_token} can't be verified due to service response misunderstanding")
    if response.model_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid token supplied')
    return response.model_id


async def get_api_key_current_user(key: str = Depends(apiKey_scheme)) -> int:
    user_id = await _verify_token(key)
    return user_id


async def get_oauth2_current_user(access_token: str = Depends(oauth2_scheme)) -> int:
    user_id = await _verify_token(access_token)
    return user_id


if settings.USE_OAUTH2_AUTHORIZATION:
    get_current_user = get_oauth2_current_user
else:
    get_current_user = get_api_key_current_user
