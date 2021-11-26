from typing import Optional, Union

from .client import redis


def get_lock(key: str, timeout: Optional[Union[int, float]] = None):
    return redis.lock(f'lock:pulse:{key}', timeout)
