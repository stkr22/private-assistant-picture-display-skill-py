"""Configuration for the Picture Display Skill."""

from private_assistant_commons import SkillConfig
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeviceMqttConfig(BaseSettings):
    """Configuration for the authenticated device MQTT broker.

    Loads from environment variables with DEVICE_MQTT_ prefix:
    - DEVICE_MQTT_HOST (default: localhost)
    - DEVICE_MQTT_PORT (default: 1883)
    - DEVICE_MQTT_USERNAME (required)
    - DEVICE_MQTT_PASSWORD (required)
    """

    model_config = SettingsConfigDict(env_prefix="DEVICE_MQTT_")

    host: str = Field(description="Device MQTT broker host")
    port: int = Field(description="Device MQTT broker port")
    username: str = Field(description="Device MQTT username for authentication")
    password: str = Field(description="Device MQTT password for authentication")


class S3Config(BaseSettings):
    """Configuration for S3-compatible image storage.

    Loads from environment variables with S3_ prefix:
    - S3_ENDPOINT (default: localhost:9000)
    - S3_BUCKET (default: inky-images)
    - S3_SECURE (default: false)
    - S3_READER_ACCESS_KEY (required)
    - S3_READER_SECRET_KEY (required)
    """

    model_config = SettingsConfigDict(env_prefix="S3_")

    endpoint: str = Field(description="S3 server endpoint")
    bucket: str = Field(default="inky-images", description="Bucket for image storage")
    secure: bool = Field(default=False, description="Use HTTPS for S3 connection")
    reader_access_key: str = Field(description="Access key for device read access")
    reader_secret_key: str = Field(description="Secret key for device read access")
    region: str | None = Field(default=None, description="S3 region (defaults to minio-py built-in)")


class PictureSkillConfig(SkillConfig):
    """Extended configuration for Picture Display Skill.

    Inherits MQTT configuration from SkillConfig and adds:
    - Default display duration for images
    - Device timeout for online status tracking
    """

    default_display_duration: int = Field(
        default=3600,
        description="Default image display duration in seconds",
    )
    device_timeout_seconds: int = Field(
        default=120,
        description="Seconds without heartbeat before device marked offline",
    )
