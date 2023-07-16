"""Файл настроек приложения."""
from logging import INFO
from typing import Any

from pydantic import AmqpDsn, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    app_title: str = "Приложение для обработки заявок"  # назван прилож
    description: str = "Прием и обработка заявок"  # описан прилож

    db_host: str
    db_port: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: PostgresDsn | None = None

    # Logging
    log_level: int | None = INFO

    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("postgres_user"),
            password=values.get("postgres_password"),
            host=values.get("db_host"),
            port=values.get("db_port"),
            path=f"/{values.get('postgres_db') or ''}",
        )

    amqp_host: str
    amqp_port: str
    rabbit_user: str
    rabbit_password: str
    celery_broker_url: AmqpDsn | None = None

    @validator("celery_broker_url", pre=True)
    def assemble_broker_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AmqpDsn.build(
            scheme="amqp",
            user=values.get("rabbit_user"),
            password=values.get("rabbit_password"),
            host=values.get("amqp_host"),
            port=values.get("amqp_port"),
        )

    celery_result_backend: str

    class Config:
        env_file = ".env"


settings = Settings()  # Пер. с экземпляром класса, для имп
