from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings 
from typing import List, Union, Optional
import os

env = os.getenv('ENVIRONMENT', None)
ENV_PATH = os.path.join(os.path.abspath(os.curdir))
ENV_FILE = '.env' if env is None else f'.env.{env}'

class Settings(BaseSettings):
    ENVIRONMENT: Optional[str] = Field(default=env, env="ENVIRONMENT")
    SECRET_KEY: str = Field('my super secret key', env='SECRET_KEY')
    BACKEND_CORS_ORIGINS: list[Union[str, AnyHttpUrl]] = []
    OPENAI_API_KEY: str = Field(default='', env='OPENAI_API_KEY')
    OPENAI_MODEL: str = Field(default='', env='OPENAI_MODEL')
    DB_URL: str = Field(default='', env='DB_URL')
    DB_NAME: str = Field(default='', env='DB_NAME')
    BASE_URL: str = Field(default='', env='BASE_URL')
    PORT: str = Field(default='', env='PORT')

    class Config:
        env_file = os.path.join(ENV_PATH, ENV_FILE)
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()