from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_NAME: str
    TEST_DB_PASS: str

    MODE: Literal["DEV", "PROD", "TEST"]

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def TEST_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}"
            f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()