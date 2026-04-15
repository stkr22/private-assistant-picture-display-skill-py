"""Configuration for the Picture Display Skill."""

from private_assistant_commons import SkillConfig
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiConfig(BaseSettings):
    """Configuration for the Picture Display API connection.

    Loads from environment variables with DISPLAY_API_ prefix:
    - DISPLAY_API_BASE_URL (required)
    - DISPLAY_API_TIMEOUT (default: 10.0)
    """

    model_config = SettingsConfigDict(env_prefix="DISPLAY_API_")

    base_url: str = Field(description="Base URL of the display API")
    timeout: float = Field(default=10.0, description="HTTP request timeout in seconds")


class PictureSkillConfig(SkillConfig):
    """Extended configuration for Picture Display Skill.

    Inherits MQTT configuration from SkillConfig.
    """
