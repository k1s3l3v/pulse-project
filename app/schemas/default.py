from pydantic import Field

from .base import BaseModel


class Version(BaseModel):
    version: str = Field(..., description='The number of version', example='1.2.3')
