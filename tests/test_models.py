"""Tests for database models."""

from datetime import datetime
from uuid import UUID, uuid4

from private_assistant_picture_display_skill.models.commands import (
    DeviceAcknowledge,
    DeviceRegistration,
    DisplayCommand,
    DisplayInfo,
    RegistrationResponse,
)
from private_assistant_picture_display_skill.models.device import DeviceDisplayState
from private_assistant_picture_display_skill.models.image import Image


class TestImageModel:
    """Tests for the Image model."""

    def test_create_image_with_required_fields(self) -> None:
        """Test creating an image with only required fields."""
        image = Image(
            source_name="manual",
            storage_path="manual/test.jpg",
        )
        assert image.source_name == "manual"
        assert image.storage_path == "manual/test.jpg"
        assert image.id is not None
        assert image.priority == 0  # default

    def test_create_image_with_all_fields(self, sample_image: Image) -> None:
        """Test creating an image with all fields."""
        assert sample_image.source_name == "manual"
        assert sample_image.title == "Test Image"
        assert sample_image.description == "A beautiful test image"
        assert sample_image.author == "Test Author"
        assert sample_image.original_width == 1600
        assert sample_image.original_height == 1200


class TestDeviceDisplayStateModel:
    """Tests for the DeviceDisplayState model."""

    def test_create_display_state(
        self, sample_display_state: DeviceDisplayState, sample_global_device_id: UUID
    ) -> None:
        """Test creating a display state."""
        assert sample_display_state.global_device_id == sample_global_device_id
        assert sample_display_state.is_online is True
        assert sample_display_state.current_image_id is not None

    def test_display_state_defaults(self) -> None:
        """Test display state default values."""
        device_id = uuid4()
        before = datetime.now()
        state = DeviceDisplayState(global_device_id=device_id)
        after = datetime.now()
        assert state.is_online is True  # default
        assert state.current_image_id is None
        assert state.displayed_since is None
        # scheduled_next_at defaults to now for immediate scheduling
        assert before <= state.scheduled_next_at <= after


class TestCommandModels:
    """Tests for MQTT command models."""

    def test_device_registration_serialization(self, sample_device_registration: DeviceRegistration) -> None:
        """Test DeviceRegistration JSON serialization."""
        json_data = sample_device_registration.model_dump_json()
        parsed = DeviceRegistration.model_validate_json(json_data)
        assert parsed.device_id == sample_device_registration.device_id
        assert parsed.display.width == sample_device_registration.display.width

    def test_device_acknowledge_serialization(self, sample_device_acknowledge: DeviceAcknowledge) -> None:
        """Test DeviceAcknowledge JSON serialization."""
        json_data = sample_device_acknowledge.model_dump_json()
        parsed = DeviceAcknowledge.model_validate_json(json_data)
        assert parsed.device_id == sample_device_acknowledge.device_id
        assert parsed.successful_display_change == sample_device_acknowledge.successful_display_change

    def test_display_command_serialization(self, sample_display_command: DisplayCommand) -> None:
        """Test DisplayCommand JSON serialization."""
        json_data = sample_display_command.model_dump_json()
        parsed = DisplayCommand.model_validate_json(json_data)
        assert parsed.action == "display"
        assert parsed.image_path == sample_display_command.image_path

    def test_registration_response_serialization(self, sample_registration_response: RegistrationResponse) -> None:
        """Test RegistrationResponse JSON serialization."""
        json_data = sample_registration_response.model_dump_json()
        parsed = RegistrationResponse.model_validate_json(json_data)
        assert parsed.status == "registered"
        assert parsed.minio_endpoint == sample_registration_response.minio_endpoint

    def test_display_info_orientation_validation(self) -> None:
        """Test DisplayInfo accepts valid orientations."""
        landscape = DisplayInfo(width=800, height=600, orientation="landscape")
        portrait = DisplayInfo(width=600, height=800, orientation="portrait")
        assert landscape.orientation == "landscape"
        assert portrait.orientation == "portrait"
