from typing import Any, Dict
from pydantic import BaseModel as BaseModel_


class BaseModel(BaseModel_):
    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        if 'exclude_unset' not in kwargs:
            kwargs['exclude_unset'] = True
        return super().dict(*args, **kwargs)


class TrimModel(BaseModel):
    class Config:
        anystr_strip_whitespace = True
