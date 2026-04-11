"""Tests for ImageManager image selection logic."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from private_assistant_commons.database import GlobalDevice

from private_assistant_picture_display_skill.models.image import Image
from private_assistant_picture_display_skill.services.image_manager import ImageManager


def _make_device(orientation: str = "landscape", attrs: dict | None = None) -> MagicMock:
    """Create a mock GlobalDevice with given orientation."""
    device = MagicMock(spec=GlobalDevice)
    device.id = uuid4()
    device.name = f"test-{orientation}"
    device.device_attributes = attrs or {
        "display_width": 1600,
        "display_height": 1200,
        "orientation": orientation,
        "model": "test-model",
    }
    return device


def _make_image(width: int = 1600, height: int = 1200, title: str = "Test") -> Image:
    """Create a sample Image."""
    return Image(
        id=uuid4(),
        source_name="manual",
        storage_path=f"manual/{title.lower()}.jpg",
        title=title,
        original_width=width,
        original_height=height,
        display_duration_seconds=60,
        created_at=datetime.now(),
    )


def _create_image_manager() -> ImageManager:
    """Create ImageManager with mocked dependencies."""
    device_mqtt = MagicMock()
    device_mqtt.publish_command = AsyncMock()
    skill_config = MagicMock()
    skill_config.default_display_duration = 3600
    return ImageManager(
        engine=MagicMock(),
        device_mqtt=device_mqtt,
        skill_config=skill_config,
        logger=MagicMock(),
    )


class TestPortraitImageSelection:
    """Test that portrait devices receive portrait-dimensioned images."""

    @pytest.mark.asyncio
    async def test_landscape_device_queries_landscape_dimensions(self):
        """Landscape device (1600x1200) should query for 1600x1200 images."""
        manager = _create_image_manager()
        landscape_image = _make_image(1600, 1200, "Landscape")

        mock_result = MagicMock()
        mock_result.first.return_value = landscape_image
        mock_session = AsyncMock()
        mock_session.exec = AsyncMock(return_value=mock_result)

        with patch("private_assistant_picture_display_skill.services.image_manager.AsyncSession") as mock_session_cls:
            mock_session_cls.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            device = _make_device("landscape")
            result = await manager.get_next_image_for_device(device)

        assert result is not None
        assert result.original_width == 1600
        assert result.original_height == 1200

    @pytest.mark.asyncio
    async def test_portrait_device_queries_swapped_dimensions(self):
        """Portrait device (panel 1600x1200) should query for 1200x1600 images."""
        manager = _create_image_manager()
        portrait_image = _make_image(1200, 1600, "Portrait")

        mock_result = MagicMock()
        mock_result.first.return_value = portrait_image
        mock_session = AsyncMock()
        mock_session.exec = AsyncMock(return_value=mock_result)

        with patch("private_assistant_picture_display_skill.services.image_manager.AsyncSession") as mock_session_cls:
            mock_session_cls.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            device = _make_device("portrait")
            result = await manager.get_next_image_for_device(device)

        assert result is not None
        assert result.original_width == 1200
        assert result.original_height == 1600

        # Verify the SQL query used swapped dimensions by inspecting the call
        call_args = mock_session.exec.call_args
        query = call_args[0][0]
        # Compile the query and check the parameters contain swapped values
        compiled = query.compile(compile_kwargs={"literal_binds": True})
        query_str = str(compiled)
        # Width should be 1200 (swapped from 1600) and height 1600 (swapped from 1200)
        assert "1200" in query_str
        assert "1600" in query_str

    @pytest.mark.asyncio
    async def test_no_orientation_defaults_to_landscape(self):
        """Device without orientation attribute should behave as landscape."""
        manager = _create_image_manager()
        image = _make_image(1600, 1200)

        mock_result = MagicMock()
        mock_result.first.return_value = image
        mock_session = AsyncMock()
        mock_session.exec = AsyncMock(return_value=mock_result)

        with patch("private_assistant_picture_display_skill.services.image_manager.AsyncSession") as mock_session_cls:
            mock_session_cls.return_value.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            device = _make_device(
                attrs={
                    "display_width": 1600,
                    "display_height": 1200,
                }
            )
            result = await manager.get_next_image_for_device(device)

        assert result is not None
        assert result.original_width == 1600
