from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SECRET_KEY_HASH: str
    SECRET_KEY_HASH_REFRESH: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ROOT_USERNAME: str
    ROOT_PASSWORD: str
    ROOT_EMAIL: EmailStr
    DATABASE_ACTIONS_URL: str


settings = Settings()
