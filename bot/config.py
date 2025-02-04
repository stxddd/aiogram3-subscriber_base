from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    MAX_TABLE_LIMIT: int
    MAX_CLIENT_LIMIT: int
    DOWNLOAD_DAY_LIMIT: int
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()