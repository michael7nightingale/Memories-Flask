from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_HOST: str
    EMAIL_PORT: int

    class Config:
        env_file = '.env'


def get_settings() -> Settings:
    return Settings()   # type: ignore
