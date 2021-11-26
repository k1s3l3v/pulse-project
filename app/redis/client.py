from redis import StrictRedis

from ..config import settings


redis = StrictRedis.from_url(settings.REDIS_URL)
