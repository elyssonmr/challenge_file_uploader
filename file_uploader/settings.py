from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    VERSION: str = '0.0.0'
    UPLOAD_FOLDER: str = 'uploads'
    BUFFER_SIZE: int = 1024 * 1024  # 1MB
    DATABASE_URL: str
