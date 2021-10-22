from .base import BaseOAuth2
from .its import ITSOAuth2
from ..db.enums import LoginServiceEnum

from typing import Type


def get_service(service: str) -> Type[BaseOAuth2]:
    service_map = {
        LoginServiceEnum.ITS.name: ITSOAuth2
    }
    return service_map[service]


def validate_service(service: str) -> bool:
    return service in LoginServiceEnum.__members__
