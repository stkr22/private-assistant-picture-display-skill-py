"""HTTP client for the Picture Display API."""

from uuid import UUID

import httpx
from pydantic import BaseModel


class DeviceInfo(BaseModel):
    """Device data returned by the display API."""

    device_id: str
    room: str | None = None
    display_width: int = 1600
    display_height: int = 1200
    display_orientation: str = "landscape"
    display_model: str = "inky_impression_13_spectra6"
    is_online: bool = False
    current_image_id: UUID | None = None


class ImageInfo(BaseModel):
    """Image metadata returned by the display API."""

    id: UUID
    title: str | None = None
    description: str | None = None
    author: str | None = None
    source_name: str | None = None


class DisplayApiClient:
    """Client for the Picture Display REST API.

    Wraps httpx.AsyncClient to provide typed access to the display API
    endpoints for device and image management.
    """

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        """Initialize the API client.

        Args:
            base_url: Base URL of the display API (e.g. http://localhost:8000).
            timeout: HTTP request timeout in seconds.

        """
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def get_devices(self) -> list[DeviceInfo]:
        """Fetch all registered devices from the API.

        Returns:
            List of devices.

        Raises:
            httpx.HTTPStatusError: On non-2xx responses.

        """
        response = await self._client.get("/api/devices")
        response.raise_for_status()
        return [DeviceInfo.model_validate(d) for d in response.json()]

    async def get_device(self, device_id: str) -> DeviceInfo | None:
        """Fetch a single device by its string identifier.

        Args:
            device_id: Device identifier (e.g. "inky-kitchen").

        Returns:
            Device info or None if not found.

        """
        response = await self._client.get(f"/api/devices/{device_id}")
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()
        return DeviceInfo.model_validate(response.json())

    async def next_image(self, device_id: str) -> ImageInfo | None:
        """Trigger FIFO image selection and push to a device.

        Calls POST /api/devices/{device_id}/next, then fetches the
        updated device and current image to return image metadata.

        Args:
            device_id: Target device identifier.

        Returns:
            Image info for voice response, or None if unavailable.

        """
        response = await self._client.post(f"/api/devices/{device_id}/next")
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()

        # Fetch updated device to get current_image_id
        device = await self.get_device(device_id)
        if device is None or device.current_image_id is None:
            return None

        return await self.get_image(device.current_image_id)

    async def get_image(self, image_id: UUID) -> ImageInfo | None:
        """Fetch image metadata by UUID.

        Args:
            image_id: Image UUID.

        Returns:
            Image info or None if not found.

        """
        response = await self._client.get(f"/api/images/{image_id}")
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()
        return ImageInfo.model_validate(response.json())
