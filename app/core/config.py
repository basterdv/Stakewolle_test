from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "Referral System API"

    # Database
    DATABASE_URL: PostgresDsn

    # Redis
    REDIS_URL: RedisDsn

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # External APIs (Optional)
    HUNTER_API_KEY: str | None = None
    CLEARBIT_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
