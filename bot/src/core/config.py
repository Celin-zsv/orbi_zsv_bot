"""Bot settings."""
from typing import Any, Callable

from pydantic import AnyHttpUrl, BaseSettings, validator


def assemble_api_url(system_name: str) -> Callable:
    def validator(v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AnyHttpUrl.build(
            scheme="http",
            host=values.get(f"{system_name}_host"),
            port=values.get(f"{system_name}_port"),
            path=values.get(f"{system_name}_path"),
        )

    return validator


class Settings(BaseSettings):
    """Bot settings."""

    telegram_api_token: str = None
    webhook_host: str = None
    webhook_path: str = None
    webhook_mode: bool = False

    expert_system_host: str
    expert_system_port: str
    expert_system_path: str
    expert_system_token: str
    api_url: AnyHttpUrl | None = None

    assemble_expert_url = validator("api_url", pre=True, allow_reuse=True)(assemble_api_url("expert_system"))

    registration_system_host: str
    registration_system_port: str
    registration_system_path: str
    registration_api_url: AnyHttpUrl | None = None

    assemble_registration_url = validator("registration_api_url", pre=True, allow_reuse=True)(
        assemble_api_url("registration_system")
    )

    amount_of_flooding_messages: int = None
    sleep_time_in_seconds: int = None

    spare_url: str = None

    class Config:
        """Config."""

        env_file = ".env"


settings = Settings()
