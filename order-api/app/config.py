from pydantic import AnyHttpUrl, BaseSettings, Field, RedisDsn


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:8080",
    ]

    USER_API_URL: AnyHttpUrl = Field(default="http://localhost:8443/users")
    USER_API_TIMEOUT: float = Field(default=5.0)

    ORDERS_INDEX: str = Field(default="orders")

    TOKEN: str = Field(default="hardcoded-token")

    REDIS_URL: RedisDsn = Field(default="redis://localhost")

    ELASTICSEARCH_HOSTS: list[AnyHttpUrl] = ["http://localhost:9200"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
