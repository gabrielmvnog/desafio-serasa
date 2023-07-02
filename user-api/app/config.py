from typing import Any

from pydantic import AnyHttpUrl, BaseSettings, Field, PostgresDsn, RedisDsn, validator


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8080",
    ]

    SECRET_KEY: str = Field(default="secretkey1234")

    ORDER_API_URL: AnyHttpUrl = Field(default="http://localhost:8443/orders")
    ORDER_API_TIMEOUT: float = Field(default=5.0)

    TOKEN: str = Field(default="hardcoded-token")

    REDIS_URL: RedisDsn = Field(default="redis://localhost")

    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="app")

    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
