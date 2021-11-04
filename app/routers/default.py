from fastapi.routing import APIRouter

from .. import schemas
from ..config import settings


router = APIRouter(prefix='', tags=['default'])


@router.get(
    '/version',
    response_model=schemas.Version
)
def get_version():
    """Get number of version"""
    return schemas.Version(version=settings.VERSION)
