"""Tests for DisplayApiClient HTTP interactions."""

from uuid import uuid4

import httpx
import pytest

from private_assistant_picture_display_skill.api_client import DeviceInfo, DisplayApiClient, ImageInfo


def _mock_transport(handler):
    """Create an httpx.MockTransport from a handler function."""
    return httpx.MockTransport(handler)


def _make_device_json(device_id: str = "inky-kitchen", is_online: bool = True, image_id: str | None = None) -> dict:
    """Build a device JSON response."""
    return {
        "id": str(uuid4()),
        "device_id": device_id,
        "room": "kitchen",
        "display_width": 1600,
        "display_height": 1200,
        "display_orientation": "landscape",
        "display_model": "test-model",
        "is_online": is_online,
        "current_image_id": image_id,
        "displayed_since": None,
        "scheduled_next_at": "2025-01-01T00:00:00",
    }


def _make_image_json(image_id: str | None = None) -> dict:
    """Build an image JSON response."""
    return {
        "id": image_id or str(uuid4()),
        "source_name": "manual",
        "storage_path": "manual/test.jpg",
        "title": "Sunset",
        "description": "A beautiful sunset",
        "author": "Photographer",
        "original_width": 1600,
        "original_height": 1200,
        "is_portrait": False,
        "display_duration_seconds": 600,
        "priority": 5,
        "last_displayed_at": None,
        "created_at": "2025-01-01T00:00:00",
        "tags": None,
    }


class TestGetDevices:
    """Tests for DisplayApiClient.get_devices."""

    @pytest.mark.asyncio
    async def test_returns_device_list(self):
        """Successful response returns parsed DeviceInfo list."""
        devices = [_make_device_json("inky-kitchen"), _make_device_json("inky-bedroom")]

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/api/devices"
            return httpx.Response(200, json=devices)

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.get_devices()
        assert len(result) == 2
        assert all(isinstance(d, DeviceInfo) for d in result)
        assert result[0].device_id == "inky-kitchen"
        assert result[1].device_id == "inky-bedroom"
        await client.close()

    @pytest.mark.asyncio
    async def test_returns_empty_list(self):
        """Empty API response returns empty list."""

        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=[])

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.get_devices()
        assert result == []
        await client.close()

    @pytest.mark.asyncio
    async def test_raises_on_server_error(self):
        """5xx response raises HTTPStatusError."""

        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, text="Internal Server Error")

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        with pytest.raises(httpx.HTTPStatusError):
            await client.get_devices()
        await client.close()


class TestGetDevice:
    """Tests for DisplayApiClient.get_device."""

    @pytest.mark.asyncio
    async def test_returns_device(self):
        """Successful response returns parsed DeviceInfo."""

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/api/devices/inky-kitchen"
            return httpx.Response(200, json=_make_device_json("inky-kitchen"))

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.get_device("inky-kitchen")
        assert result is not None
        assert result.device_id == "inky-kitchen"
        await client.close()

    @pytest.mark.asyncio
    async def test_returns_none_on_404(self):
        """404 response returns None."""

        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"detail": "Device not found"})

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.get_device("nonexistent")
        assert result is None
        await client.close()


class TestNextImage:
    """Tests for DisplayApiClient.next_image."""

    @pytest.mark.asyncio
    async def test_returns_image_info(self):
        """Successful next triggers image fetch chain."""
        image_id = str(uuid4())
        device_json = _make_device_json("inky-kitchen", image_id=image_id)
        image_json = _make_image_json(image_id)

        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "POST" and request.url.path == "/api/devices/inky-kitchen/next":
                return httpx.Response(200, json={"status": "ok"})
            if request.method == "GET" and request.url.path == "/api/devices/inky-kitchen":
                return httpx.Response(200, json=device_json)
            if request.method == "GET" and f"/api/images/{image_id}" in str(request.url):
                return httpx.Response(200, json=image_json)
            return httpx.Response(404)

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.next_image("inky-kitchen")
        assert result is not None
        assert isinstance(result, ImageInfo)
        assert result.title == "Sunset"
        await client.close()

    @pytest.mark.asyncio
    async def test_returns_none_when_device_not_connected(self):
        """404 on /next returns None."""

        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"detail": "Device not connected"})

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.next_image("offline-device")
        assert result is None
        await client.close()

    @pytest.mark.asyncio
    async def test_returns_none_when_no_image_available(self):
        """404 on /next when no suitable image exists returns None."""

        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "POST":
                return httpx.Response(404, json={"detail": "No suitable image available"})
            return httpx.Response(404)

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.next_image("inky-kitchen")
        assert result is None
        await client.close()


class TestGetImage:
    """Tests for DisplayApiClient.get_image."""

    @pytest.mark.asyncio
    async def test_returns_image_info(self):
        """Successful response returns parsed ImageInfo."""
        image_id = uuid4()

        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=_make_image_json(str(image_id)))

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.get_image(image_id)
        assert result is not None
        assert isinstance(result, ImageInfo)
        assert result.title == "Sunset"
        assert result.description == "A beautiful sunset"
        assert result.author == "Photographer"
        await client.close()

    @pytest.mark.asyncio
    async def test_returns_none_on_404(self):
        """404 response returns None."""
        image_id = uuid4()

        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"detail": "Image not found"})

        client = DisplayApiClient.__new__(DisplayApiClient)
        client._client = httpx.AsyncClient(transport=_mock_transport(handler), base_url="http://test")

        result = await client.get_image(image_id)
        assert result is None
        await client.close()
