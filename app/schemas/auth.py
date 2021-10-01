from enum import Enum
from pydantic import Field

from .base import BaseModel


class AuthGrantType(str, Enum):
    authorization_code = 'authorization_code'
    refresh_token = 'refresh_token'


class AccessToken(BaseModel):
    access_token: str = Field(..., description='The access token')
    refresh_token: str = Field(None, description='The refresh token')
    expires_in: int = Field(None, description='The token expires in')
    # staff: Staff = Field(..., description='The staff related to access token')
