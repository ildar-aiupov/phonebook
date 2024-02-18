from logging import config as logging_config

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)
load_dotenv()


class Settings(BaseSettings):
    redis_host: str = "redis"
    redis_port: int = 6379
    show_openapi_docs: bool = True


settings = Settings()
