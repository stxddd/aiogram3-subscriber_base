from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    ADMIN_TG_ID: int
    ADMIN_USERNAME: str

    MARZBAN_URL: str
    MARZBAN_USER: str
    MARZBAN_PASS: str
    MARZBAN_REQUEST_DAY_LIMIT: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    TZ: str

    HOUR_TO_RECEIVE_NOTIFICATIONS: int
    MINUTE_TO_RECEIVE_NOTIFICATIONS: int

    ONE_MONTH_PRICE: int
    THREE_MONTH_PRICE: int
    SIX_MONTH_PRICE: int
    ONE_YEAR_PRICE: int

    KEY_FOR_DELETE: str

    PAYMENT_LINK: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
