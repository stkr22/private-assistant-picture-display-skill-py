"""Pytest fixtures for Picture Display Skill tests."""

from datetime import datetime
from uuid import UUID, uuid4

import pytest

from private_assistant_picture_display_skill.config import DeviceMqttConfig, MinioConfig, PictureSkillConfig
from private_assistant_picture_display_skill.models.commands import (
    DeviceAcknowledge,
    DeviceRegistration,
    DisplayCommand,
    DisplayInfo,
    RegistrationResponse,
)
from private_assistant_picture_display_skill.models.device import DeviceDisplayState
from private_assistant_picture_display_skill.models.image import Image


@pytest.fixture
def sample_image() -> Image:
    """Create a sample Image for testing."""
    return Image(
        id=uuid4(),
        source_name="manual",
        storage_path="manual/test-image.jpg",
        title="Test Image",
        description="A beautiful test image",
        author="Test Author",
        original_width=1600,
        original_height=1200,
        fetched_at=datetime.now(),
    )


@pytest.fixture
def sample_global_device_id() -> UUID:
    """Create a sample global device ID for testing."""
    return uuid4()


@pytest.fixture
def sample_display_state(sample_image: Image, sample_global_device_id: UUID) -> DeviceDisplayState:
    """Create a sample DeviceDisplayState for testing."""
    return DeviceDisplayState(
        global_device_id=sample_global_device_id,
        is_online=True,
        current_image_id=sample_image.id,
        displayed_since=datetime.now(),
        scheduled_next_at=datetime.now(),
    )


@pytest.fixture
def sample_device_registration() -> DeviceRegistration:
    """Create a sample DeviceRegistration for testing."""
    return DeviceRegistration(
        device_id="inky-kitchen",
        display=DisplayInfo(
            width=1600,
            height=1200,
            orientation="landscape",
            model="impression-13.3-spectra6",
        ),
        room="kitchen",
    )


@pytest.fixture
def sample_device_acknowledge() -> DeviceAcknowledge:
    """Create a sample DeviceAcknowledge for testing."""
    return DeviceAcknowledge(
        device_id="inky-livingroom",
        image_id=str(uuid4()),
        successful_display_change=True,
    )


@pytest.fixture
def sample_display_command() -> DisplayCommand:
    """Create a sample DisplayCommand for testing."""
    return DisplayCommand(
        action="display",
        image_path="manual/test-image.jpg",
        image_id=str(uuid4()),
        title="Test Image",
    )


@pytest.fixture
def sample_registration_response() -> RegistrationResponse:
    """Create a sample RegistrationResponse for testing."""
    return RegistrationResponse(
        status="registered",
        minio_endpoint="localhost:9000",
        minio_bucket="inky-images",
        minio_access_key="test-access-key",
        minio_secret_key="test-secret-key",
        minio_secure=False,
    )


@pytest.fixture
def device_mqtt_config() -> DeviceMqttConfig:
    """Create a DeviceMqttConfig for testing."""
    return DeviceMqttConfig(
        host="localhost",
        port=1883,
        username="test-user",
        password="test-password",
    )


@pytest.fixture
def minio_config() -> MinioConfig:
    """Create a MinioConfig for testing."""
    return MinioConfig(
        endpoint="localhost:9000",
        bucket="inky-images",
        secure=False,
        reader_access_key="test-access-key",
        reader_secret_key="test-secret-key",
    )


@pytest.fixture
def skill_config() -> PictureSkillConfig:
    """Create a PictureSkillConfig for testing."""
    return PictureSkillConfig(
        client_id="picture-display-skill-test",
        default_display_duration=3600,
        device_timeout_seconds=120,
    )
