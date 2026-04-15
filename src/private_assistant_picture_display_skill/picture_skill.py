"""Picture Display Skill for controlling Inky e-ink displays via the display API."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import httpx
import jinja2
from private_assistant_commons import BaseSkill, IntentRequest, IntentType
from private_assistant_commons.database import GlobalDevice
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

if TYPE_CHECKING:
    import logging
    from uuid import UUID

    import aiomqtt
    from sqlalchemy.ext.asyncio import AsyncEngine

from private_assistant_picture_display_skill.api_client import DisplayApiClient, ImageInfo
from private_assistant_picture_display_skill.config import ApiConfig, PictureSkillConfig


class PictureSkill(BaseSkill):
    """Voice-controlled picture display skill for Inky e-ink devices.

    Handles voice commands to control image display on Inky devices:
    - "next picture" / "show next" - Display next image in queue
    - "what am I seeing?" / "describe this picture" - Describe current image

    Delegates all device and image management to the display API over HTTP.
    """

    help_text = (
        "You can control the picture display with these commands. "
        'Say "next picture" to show the next image. '
        'Say "what am I seeing" to hear a description of the current picture.'
    )

    # Device sync interval in seconds
    device_sync_interval: int = 60

    def __init__(  # noqa: PLR0913
        self,
        config_obj: PictureSkillConfig,
        mqtt_client: aiomqtt.Client,
        task_group: asyncio.TaskGroup,
        engine: AsyncEngine,
        logger: logging.Logger | None = None,
        template_env: jinja2.Environment | None = None,
    ) -> None:
        """Initialize the Picture Display Skill.

        Args:
            config_obj: Skill configuration (inherits from SkillConfig)
            mqtt_client: Internal MQTT client (from BaseSkill)
            task_group: Asyncio task group for concurrent operations
            engine: Async database engine
            logger: Optional custom logger
            template_env: Jinja2 template environment for voice responses

        """
        super().__init__(
            config_obj=config_obj,
            mqtt_client=mqtt_client,
            task_group=task_group,
            engine=engine,
            certainty_threshold=0.7,
            logger=logger,
        )

        self.skill_config = config_obj

        # Display API client
        self.api_config = ApiConfig()  # ty: ignore[missing-argument]
        self.api_client = DisplayApiClient(
            base_url=self.api_config.base_url,
            timeout=self.api_config.timeout,
        )

        self.supported_intents = {
            IntentType.MEDIA_NEXT: 0.8,
            IntentType.DEVICE_QUERY: 0.7,
        }

        self.supported_device_types = ["picture_display"]

        if template_env is not None:
            self.template_env = template_env
        else:
            self.template_env = jinja2.Environment(
                loader=jinja2.PackageLoader("private_assistant_picture_display_skill", "templates"),
                autoescape=True,
            )

    async def skill_preparations(self) -> None:
        """Initialize services after MQTT setup."""
        await super().skill_preparations()

        # Sync devices from the display API into GlobalDevice registry
        await self._sync_devices_from_api()

        # Start periodic device sync
        self.add_task(self._periodic_device_sync(), name="device_sync")

        self.logger.info("Picture skill preparations complete")

    async def _periodic_device_sync(self) -> None:
        """Background task to periodically sync devices from the API."""
        while True:
            await asyncio.sleep(self.device_sync_interval)
            try:
                await self._sync_devices_from_api()
            except Exception as e:
                self.logger.error("Error in device sync: %s", e, exc_info=True)

    async def _sync_devices_from_api(self) -> None:
        """Fetch devices from the display API and register/update in GlobalDevice."""
        try:
            api_devices = await self.api_client.get_devices()
        except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
            self.logger.error("Failed to fetch devices from API: %s", e)
            return

        for api_device in api_devices:
            device_attributes = {
                "display_width": api_device.display_width,
                "display_height": api_device.display_height,
                "orientation": api_device.display_orientation,
                "model": api_device.display_model,
                "is_online": api_device.is_online,
            }

            patterns = [api_device.device_id]
            if api_device.room:
                patterns.extend(
                    [
                        f"{api_device.room} display",
                        f"{api_device.room} picture frame",
                        f"display in {api_device.room}",
                    ]
                )

            existing = self._find_device_by_name(api_device.device_id)
            if existing:
                await self._update_device(existing.id, device_attributes, patterns)
            else:
                await self.register_device(
                    device_type="picture_display",
                    name=api_device.device_id,
                    pattern=patterns,
                    room=api_device.room,
                    device_attributes=device_attributes,
                )

        self.logger.debug("Synced %d devices from API", len(api_devices))

    def _find_device_by_name(self, name: str) -> GlobalDevice | None:
        """Find a device in the global_devices cache by name.

        Args:
            name: Device name to search for

        Returns:
            GlobalDevice if found, None otherwise

        """
        device: GlobalDevice
        for device in self.global_devices:
            if device.name == name:
                return device
        return None

    async def _update_device(self, device_id: UUID, device_attributes: dict, patterns: list[str]) -> UUID:
        """Update an existing device's attributes and patterns.

        Args:
            device_id: GlobalDevice UUID
            device_attributes: New device attributes
            patterns: New pattern list

        Returns:
            The device UUID

        """
        async with AsyncSession(self.engine) as session:
            result = await session.exec(select(GlobalDevice).where(GlobalDevice.id == device_id))
            device = result.first()
            if device:
                device.device_attributes = device_attributes
                device.pattern = patterns
                await session.commit()

        self.global_devices = await self.get_skill_devices()

        return device_id

    async def process_request(self, intent_request: IntentRequest) -> None:
        """Process voice command intent.

        Args:
            intent_request: Validated intent request

        """
        intent_type = intent_request.classified_intent.intent_type

        match intent_type:
            case IntentType.MEDIA_NEXT:
                await self._handle_media_next(intent_request)
            case IntentType.DEVICE_QUERY:
                await self._handle_query_status(intent_request)
            case _:
                self.logger.warning("Unhandled intent type: %s", intent_type)

    async def _select_devices_for_request(self, intent_request: IntentRequest) -> list[GlobalDevice]:
        """Select appropriate devices based on room or explicit naming.

        Priority:
        1. Explicitly named device in entities (single device)
        2. All online devices in the same room as request
        3. First online device (fallback)

        Args:
            intent_request: Intent request with client info and entities

        Returns:
            List of matching online GlobalDevices, may be empty

        """
        device: GlobalDevice

        # Check for explicit device name in entities
        device_entities = intent_request.classified_intent.entities.get("device", [])
        if device_entities:
            device_name = device_entities[0].normalized_value
            for device in self.global_devices:
                if device_name.lower() in [p.lower() for p in device.pattern] and self._is_device_online(device):
                    self.logger.debug("Selected device by name: %s", device.name)
                    return [device]

        # Room-based selection: collect all online devices in the room
        request_room = intent_request.client_request.room
        if request_room:
            room_devices: list[GlobalDevice] = []
            for device in self.global_devices:
                if device.room and device.room.name == request_room and self._is_device_online(device):
                    room_devices.append(device)
            if room_devices:
                self.logger.debug(
                    "Selected %d device(s) in room %s: %s",
                    len(room_devices),
                    request_room,
                    [d.name for d in room_devices],
                )
                return room_devices

        # Fallback: first online device
        for device in self.global_devices:
            if self._is_device_online(device):
                self.logger.debug("Selected first online device: %s", device.name)
                return [device]

        return []

    @staticmethod
    def _is_device_online(device: GlobalDevice) -> bool:
        """Check if a device is online based on synced attributes.

        Args:
            device: GlobalDevice with device_attributes from API sync

        Returns:
            True if device is online

        """
        attrs = device.device_attributes or {}
        return attrs.get("is_online", False)

    async def _handle_media_next(self, intent_request: IntentRequest) -> None:
        """Handle 'next picture' command.

        Args:
            intent_request: Intent request with client info

        """
        devices = await self._select_devices_for_request(intent_request)
        if not devices:
            await self.send_response(
                "No picture displays are currently online.",
                intent_request.client_request,
            )
            return

        last_image: ImageInfo | None = None
        for device in devices:
            try:
                image = await self.api_client.next_image(device.name)
            except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
                self.logger.error("API error advancing image on %s: %s", device.name, e)
                continue

            if image is not None:
                last_image = image
            else:
                self.logger.warning("No images available for device %s", device.name)

        if last_image is None:
            await self.send_response(
                "No images available to display.",
                intent_request.client_request,
            )
            return

        template = self.template_env.get_template("next_picture.j2")
        response_text = template.render(image=last_image)
        await self.send_response(response_text, intent_request.client_request)

    async def _handle_query_status(self, intent_request: IntentRequest) -> None:
        """Handle 'what am I seeing?' command.

        Args:
            intent_request: Intent request with client info

        """
        devices = await self._select_devices_for_request(intent_request)
        if not devices:
            await self.send_response(
                "No picture displays are currently online.",
                intent_request.client_request,
            )
            return
        device = devices[0]

        try:
            api_device = await self.api_client.get_device(device.name)
        except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
            self.logger.error("API error fetching device %s: %s", device.name, e)
            await self.send_response(
                "Picture display service is temporarily unavailable.",
                intent_request.client_request,
            )
            return

        if api_device is None or api_device.current_image_id is None:
            await self.send_response(
                "No image is currently being displayed.",
                intent_request.client_request,
            )
            return

        try:
            image = await self.api_client.get_image(api_device.current_image_id)
        except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
            self.logger.error("API error fetching image: %s", e)
            await self.send_response(
                "Picture display service is temporarily unavailable.",
                intent_request.client_request,
            )
            return

        if image is None:
            await self.send_response(
                "No image is currently being displayed.",
                intent_request.client_request,
            )
            return

        template = self.template_env.get_template("describe_image.j2")
        response_text = template.render(image=image)
        await self.send_response(response_text, intent_request.client_request)
