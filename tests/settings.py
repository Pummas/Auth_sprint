from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: str = Field("6379", env="REDIS_PORT")
    base_api: str = Field("http://127.0.0.1:5000", env="BASE_API")
