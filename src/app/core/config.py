from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SECRET_KEY_HASH: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ROOT_USERNAME: str
    ROOT_PASSWORD: str
    ROOT_EMAIL: EmailStr
    DATABASE_ACTIONS_URL: str
    RENDER_DB_PASSWORD: str
    RENDER_DB_HOST: str
    RENDER_DB_USER: str
    RENDER_DB_NAME: str
    RENDER_DB_PORT: int


settings = Settings()
