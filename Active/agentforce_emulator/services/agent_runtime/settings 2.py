"""Settings for agent runtime service."""

from __future__ import annotations

from pathlib import Path

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    crm_api_url: AnyUrl = Field(default="http://localhost:8001")
    redis_url: AnyUrl = Field(default="redis://localhost:6380/0")
    scoring_config_path: Path = Field(
        default=ROOT_DIR / "configs" / "scoring_rules.yaml"
    )
    agent_settings_path: Path = Field(
        default=ROOT_DIR / "configs" / "agent_settings.yaml"
    )
    default_model_provider: str = Field(default="openai")


settings = Settings()


__all__ = ["settings", "Settings"]


