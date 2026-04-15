"""Pytest fixtures for Picture Display Skill tests."""

from uuid import uuid4

import pytest

from private_assistant_picture_display_skill.api_client import DeviceInfo, ImageInfo
from private_assistant_picture_display_skill.config import PictureSkillConfig


@pytest.fixture
def sample_device_info() -> DeviceInfo:
    """Create a sample DeviceInfo matching the display API response."""
    return DeviceInfo(
        device_id="inky-kitchen",
        room="kitchen",
        display_width=1600,
        display_height=1200,
        display_orientation="landscape",
        display_model="impression-13.3-spectra6",
        is_online=True,
        current_image_id=uuid4(),
    )


@pytest.fixture
def sample_image_info() -> ImageInfo:
    """Create a sample ImageInfo matching the display API response."""
    return ImageInfo(
        id=uuid4(),
        title="Test Image",
        description="A beautiful test image",
        author="Test Author",
        source_name="manual",
    )


@pytest.fixture
def skill_config() -> PictureSkillConfig:
    """Create a PictureSkillConfig for testing."""
    return PictureSkillConfig(
        client_id="picture-display-skill-test",
    )
