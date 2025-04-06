from pathlib import Path
from typing import List, Literal, Optional, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).parent.parent


class Config(BaseSettings):
    # Конфигурация для переменных окружения
    model_config = SettingsConfigDict(
        env_file=[".dev.env", ".env.test", ".env"],
        env_file_encoding="utf-8",
    )

    BOT_TOKEN: str = Field(alias="TOKEN")

    # Настройки для логирования
    LOG_LEVEL: Literal["info", "debug", "warning", "error"] = "info"
    LOG_FILENAME: Path = Field(default=BASE_DIR.parent / "logger.log")
    LOG_FORMAT: str = Field(
        default="%(levelname)-10s%(asctime)-25s %(name)s - %(funcName)-15s: %(lineno)-5d - %(message)3s"
    )

    # Общие настройки
    ADMIN_IDS: List[Optional[int]]


# Пример использования
settings = Config()
