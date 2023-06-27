from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = '.env'


def get_settings() -> BaseSettings:
    return Settings()   # type: ignore
