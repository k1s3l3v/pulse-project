from typing import List
from pydantic import AnyHttpUrl, BaseSettings, RedisDsn, PostgresDsn


class Settings(BaseSettings):
    VERSION: str = '0.0.1'

    DATABASE_URI: PostgresDsn

    CORS_ORIGINS: List[AnyHttpUrl] = []

    LOG: bool = False

    PORT: int = 5000
    URL_PREFIX: str = '/api/v1'

    ITS_CLIENT_ID: str = ''  # TODO: fill ID
    ITS_CLIENT_SECRET: str

    CELERY_BROKER_URL: RedisDsn = 'redis://127.0.0.1:6379/1'
    CELERY_IMPORTS: List[str] = ['app.tasks']
    CELERY_TIMEZONE = 'Europe/Moscow'

    USE_OAUTH2_AUTHORIZATION: bool = True

    class Config:
        case_sensitive = True
        env_file = 'api.env'
        env_prefix = 'API_'


settings = Settings()
