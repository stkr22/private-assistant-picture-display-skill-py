"""Immich integration for fetching images from self-hosted Immich instances."""

from private_assistant_picture_display_skill.immich.client import ImmichClient
from private_assistant_picture_display_skill.immich.config import (
    DeviceRequirements,
    ImmichConnectionConfig,
    ImmichSyncConfig,
    S3WriterConfig,
)
from private_assistant_picture_display_skill.immich.sync_service import ImmichSyncService

__all__ = [
    "DeviceRequirements",
    "ImmichClient",
    "ImmichConnectionConfig",
    "ImmichSyncConfig",
    "ImmichSyncService",
    "S3WriterConfig",
]
