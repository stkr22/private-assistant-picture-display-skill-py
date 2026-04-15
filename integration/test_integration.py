"""End-to-end integration tests for the Picture Display Skill.

These tests validate the complete skill workflow with real external services:
- PostgreSQL database (GlobalDevice registry)
- MQTT broker (intent engine message bus)
- Display API (device and image management)
- Picture skill running in background

Test flow:
1. Start skill in background (connected to PostgreSQL + MQTT + display API)
2. Publish IntentRequest to MQTT
3. Assert skill publishes correct voice responses

Run these tests with:
    pytest integration/test_integration.py -v -m integration

Requirements:
- Compose services (PostgreSQL, Mosquitto) must be running
- Display API must be running and accessible at DISPLAY_API_BASE_URL
"""

import pytest

# Mark all tests in this module as integration tests
# These tests require external services and are skipped by default
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skip(reason="Requires display API test service — to be rewritten"),
]


class TestMediaNextCommand:
    """Test next picture command (MEDIA_NEXT)."""

    @pytest.mark.asyncio
    async def test_next_picture_sends_voice_response(self):
        """Test MEDIA_NEXT triggers API call and returns voice response."""

    @pytest.mark.asyncio
    async def test_next_picture_no_devices_online(self):
        """Test MEDIA_NEXT when no devices are online returns appropriate message."""


class TestQueryStatusCommand:
    """Test device query command (DEVICE_QUERY)."""

    @pytest.mark.asyncio
    async def test_describe_current_image(self):
        """Test DEVICE_QUERY returns description of currently displayed image."""

    @pytest.mark.asyncio
    async def test_describe_no_image_displayed(self):
        """Test DEVICE_QUERY when no image is displayed returns appropriate message."""
