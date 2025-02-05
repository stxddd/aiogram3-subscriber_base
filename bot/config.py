from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    FLOOD_THRESHOLD: int

    MAX_TABLE_LIMIT: int
    MAX_CLIENT_LIMIT: int
    DOWNLOAD_DAY_LIMIT: int

    TIME_TO_RECEIVE_NOTIFICATIONS: int

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
