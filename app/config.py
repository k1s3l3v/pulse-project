from pydantic import AnyHttpUrl, BaseSettings, Field, RedisDsn, PostgresDsn
from typing import List, Optional


class Settings(BaseSettings):
    VERSION: str = '0.0.1'

    DATABASE_URI: PostgresDsn

    CORS_ORIGINS: List[AnyHttpUrl] = []

    LOG: bool = False

    PORT: int = 5000
    URL_PREFIX: str = '/pulse/api/v1'
    ADMIN_URL_PREFIX: str = '/pulse'

    CELERY_BROKER_URL: RedisDsn = 'redis://127.0.0.1:6379/1'
    CELERY_IMPORTS: List[str] = ['app.celery.tasks']
    CELERY_TIMEZONE = 'Europe/Moscow'

    ITS_CLIENT_ID: str = Field('', env='ITS_CLIENT_ID')  # TODO: fill ID
    USE_OAUTH2_AUTHORIZATION: bool = Field(True, env='USE_OAUTH2_AUTHORIZATION')

    BROKER_HOST: str = Field('127.0.0.1', env='BROKER_HOST')
    BROKER_PORT: int = Field(5672, env='BROKER_PORT')
    BROKER_LOGIN: str = Field('guest', env='BROKER_LOGIN')
    BROKER_PASSWORD: str = Field('guest', env='BROKER_PASSWORD')
    BROKER_SERVICE_QUEUE: str = 'rpc_pulse_queue'
    BROKER_CLIENT_QUEUE: Optional[str] = BROKER_SERVICE_QUEUE
    STAFF_BROKER_SERVICE_QUEUE: str = Field('rpc_staff_queue', env='STAFF_BROKER_SERVICE_QUEUE')

    FLASK_ADMIN_SWATCH: str = 'cosmo'
    SECURITY_REGISTERABLE: str = True
    SECURITY_PASSWORD_SALT: str
    SECRET_KEY: str

    ADMIN_USER_NAME: str
    ADMIN_USER_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = 'pulse.env'
        env_prefix = 'PULSE_'


settings = Settings()
