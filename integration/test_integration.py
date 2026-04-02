"""End-to-end integration tests for the Picture Display Skill.

These tests validate the complete skill workflow with real external services:
- PostgreSQL database (device and image registry)
- MQTT broker (message bus)
- Picture skill running in background

Test flow:
1. Setup database with test images and devices
2. Start skill in background
3. Publish IntentRequest to MQTT
4. Assert skill publishes correct responses

Run these tests with:
    pytest tests/test_integration.py -v -m integration

Requirements:
- Compose services (PostgreSQL, Mosquitto) must be running
"""

import asyncio
import contextlib
import json
import logging
import os
import uuid
from collections.abc import AsyncGenerator
from datetime import datetime, timedelta

import aiomqtt
import pytest
import yaml
from private_assistant_commons import (
    ClassifiedIntent,
    ClientRequest,
    IntentRequest,
    IntentType,
    create_skill_engine,
)
from private_assistant_commons.database import DeviceType, GlobalDevice, Skill
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from private_assistant_picture_display_skill.main import start_skill
from private_assistant_picture_display_skill.models.device import DeviceDisplayState
from private_assistant_picture_display_skill.models.image import Image
from private_assistant_picture_display_skill.picture_skill import PictureSkill

# Mark all tests in this module as integration tests
# These tests require external services and are skipped by default
pytestmark = [pytest.mark.integration]

# Logger for test debugging
logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
async def db_engine():
    """Create a database engine for integration tests."""
    engine = create_skill_engine(echo=False)

    # Ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Cleanup: Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    """Create a database session for each test."""
    async with AsyncSession(db_engine) as session:
        yield session


@pytest.fixture
def mqtt_config():
    """Get MQTT configuration from environment variables."""
    return {
        "host": os.getenv("MQTT_HOST", "mosquitto"),
        "port": int(os.getenv("MQTT_PORT", "1883")),
    }


@pytest.fixture
async def mqtt_test_client(mqtt_config):
    """Create an MQTT test client."""
    async with aiomqtt.Client(hostname=mqtt_config["host"], port=mqtt_config["port"]) as client:
        yield client


@pytest.fixture
async def test_image(db_session) -> AsyncGenerator[Image, None]:
    """Create a test image in the database."""
    image = Image(
        id=uuid.uuid4(),
        source_name="manual",
        storage_path="manual/test-image.jpg",
        title="Test Landscape",
        description="A beautiful mountain landscape for testing",
        author="Test Photographer",
        original_width=1600,
        original_height=1200,
        display_duration_seconds=60,
        created_at=datetime.now(),
    )
    db_session.add(image)
    await db_session.commit()
    await db_session.refresh(image)

    logger.debug("Test image created: %s", image.id)

    yield image

    # Cleanup
    await db_session.delete(image)
    await db_session.commit()


@pytest.fixture
async def test_device(db_session) -> AsyncGenerator[GlobalDevice, None]:
    """Create a test picture device in the database using GlobalDevice.

    Device attributes (display dimensions, etc.) are stored in device_attributes JSON.
    """
    # Create DeviceType first (required FK)
    device_type = DeviceType(name="picture_display")
    db_session.add(device_type)

    # Create Skill first (required FK)
    skill = Skill(name="picture-display-skill")
    db_session.add(skill)

    await db_session.commit()
    await db_session.refresh(device_type)
    await db_session.refresh(skill)

    device_id = uuid.uuid4()
    device = GlobalDevice(
        id=device_id,
        device_type_id=device_type.id,
        skill_id=skill.id,
        name="inky-test",
        pattern=["inky-test", "test display"],
        device_attributes={
            "display_width": 1600,
            "display_height": 1200,
            "orientation": "landscape",
            "model": "impression-13.3-spectra6",
        },
    )
    db_session.add(device)

    # Create display state (linked to GlobalDevice)
    display_state = DeviceDisplayState(global_device_id=device_id, is_online=True)
    db_session.add(display_state)

    await db_session.commit()
    await db_session.refresh(device)

    logger.debug("Test device created: %s (id=%s)", device.name, device.id)

    yield device

    # Cleanup (order matters for FK constraints)
    await db_session.delete(display_state)
    await db_session.delete(device)
    await db_session.delete(skill)
    await db_session.delete(device_type)
    await db_session.commit()


@pytest.fixture
async def skill_config_file(mqtt_config, tmp_path):  # noqa: ARG001
    """Create a temporary config file for the skill.

    Note: MQTT configuration is now handled via environment variables
    through MqttConfig, not in the YAML config file.
    """
    config = {
        "client_id": "picture-display-skill-integration-test",
        "base_topic": "assistant",
    }

    config_path = tmp_path / "skill_config.yaml"
    with config_path.open("w") as f:
        yaml.dump(config, f)

    yield config_path


@pytest.fixture
async def running_skill(
    test_image,  # noqa: ARG001
    test_device,  # noqa: ARG001
    db_engine,  # noqa: ARG001
    skill_config_file,
    mqtt_config,
):
    """Start the skill in background with test data ready.

    The test_image, test_device, and db_engine fixtures are dependencies
    that ensure the database is set up before the skill starts.
    """
    # Give database time to fully persist the commits
    await asyncio.sleep(0.5)

    # Set environment variables for the skill
    os.environ["MQTT_HOST"] = mqtt_config["host"]
    os.environ["MQTT_PORT"] = str(mqtt_config["port"])
    os.environ["DEVICE_MQTT_HOST"] = mqtt_config["host"]
    os.environ["DEVICE_MQTT_PORT"] = str(mqtt_config["port"])
    os.environ["DEVICE_MQTT_USERNAME"] = ""
    os.environ["DEVICE_MQTT_PASSWORD"] = ""
    os.environ["S3_ENDPOINT"] = "localhost:9000"
    os.environ["S3_BUCKET"] = "inky-images"
    os.environ["S3_READER_ACCESS_KEY"] = ""
    os.environ["S3_READER_SECRET_KEY"] = ""

    # Start skill as background task with config file path
    skill_task = asyncio.create_task(start_skill(skill_config_file))

    # Wait for skill to initialize and subscribe to all topics
    await asyncio.sleep(3)

    yield

    # Cleanup: Cancel skill task
    skill_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await skill_task


class TestMediaNextCommand:
    """Test next picture command (MEDIA_NEXT)."""

    @pytest.mark.asyncio
    async def test_next_picture_no_devices(
        self,
        running_skill,  # noqa: ARG002
        mqtt_test_client,
        db_session,
    ):
        """Test MEDIA_NEXT when no devices are online returns appropriate message.

        Flow:
        1. Mark all devices as offline
        2. Publish IntentRequest with MEDIA_NEXT intent
        3. Assert response indicates no devices online
        """
        # Mark test device as offline via DeviceDisplayState
        result = await db_session.exec(select(DeviceDisplayState))
        display_states = result.all()
        for state in display_states:
            state.is_online = False
        await db_session.commit()

        output_topic = f"assistant/test/output/{uuid.uuid4().hex[:8]}"
        await mqtt_test_client.subscribe(output_topic)

        classified_intent = ClassifiedIntent(
            id=uuid.uuid4(),
            intent_type=IntentType.MEDIA_NEXT,
            confidence=0.9,
            entities={},
            alternative_intents=[],
            raw_text="next picture",
            timestamp=datetime.now(),
        )

        client_request = ClientRequest(
            id=uuid.uuid4(),
            text="next picture",
            room="test",
            output_topic=output_topic,
        )

        intent_request = IntentRequest(
            id=uuid.uuid4(),
            classified_intent=classified_intent,
            client_request=client_request,
        )

        intent_json = intent_request.model_dump_json()
        await mqtt_test_client.publish("assistant/intent_engine/result", intent_json, qos=1)

        response_received = False
        timeout_seconds = 5

        try:
            async with asyncio.timeout(timeout_seconds):
                async for message in mqtt_test_client.messages:
                    topic = str(message.topic)
                    payload = message.payload.decode()

                    if topic == output_topic:
                        # Should indicate no devices online
                        assert "online" in payload.lower() or "no" in payload.lower()
                        response_received = True
                        logger.debug("Response received: %s", payload)
                        break

        except TimeoutError:
            pass

        assert response_received, "Did not receive response within timeout"


@pytest.fixture
async def rotation_test_setup(db_engine, skill_config_file, mqtt_config):
    """Set up everything for rotation testing.

    Creates images, device, display state, and starts skill - all in one fixture
    to avoid session sharing issues between fixtures.
    """
    # Create a fresh session for setup
    async with AsyncSession(db_engine) as session:
        # Create images
        current_image = Image(
            id=uuid.uuid4(),
            source_name="manual",
            storage_path="manual/current-image.jpg",
            title="Current Image",
            description="Currently displayed image",
            original_width=1600,
            original_height=1200,
            display_duration_seconds=60,
            created_at=datetime.now() - timedelta(days=1),
            last_displayed_at=datetime.now() - timedelta(hours=1),
        )
        session.add(current_image)

        next_image = Image(
            id=uuid.uuid4(),
            source_name="manual",
            storage_path="manual/next-image.jpg",
            title="Next Image",
            description="Image to be displayed next",
            original_width=1600,
            original_height=1200,
            display_duration_seconds=60,
            created_at=datetime.now(),
            last_displayed_at=None,
        )
        session.add(next_image)

        # Create DeviceType and Skill
        device_type = DeviceType(name="picture_display")
        session.add(device_type)

        skill_record = Skill(name="picture-display-skill-integration-test")
        session.add(skill_record)

        await session.commit()
        await session.refresh(current_image)
        await session.refresh(next_image)
        await session.refresh(device_type)
        await session.refresh(skill_record)

        # Create device
        device_id = uuid.uuid4()
        device = GlobalDevice(
            id=device_id,
            device_type_id=device_type.id,
            skill_id=skill_record.id,
            name="inky-test",
            pattern=["inky-test", "test display"],
            device_attributes={
                "display_width": 1600,
                "display_height": 1200,
                "orientation": "landscape",
                "model": "impression-13.3-spectra6",
            },
        )
        session.add(device)

        # Create display state due for rotation
        display_state = DeviceDisplayState(
            global_device_id=device_id,
            is_online=True,
            current_image_id=current_image.id,
            displayed_since=datetime.now() - timedelta(hours=2),
            scheduled_next_at=datetime.now() - timedelta(hours=1),
        )
        session.add(display_state)

        await session.commit()

        # Store next_image id for test assertion (must do before session closes)
        await session.refresh(next_image)
        next_image_id = next_image.id

    # Give database time to persist
    await asyncio.sleep(0.5)

    # Monkeypatch rotation interval for fast testing
    original_interval = PictureSkill.rotation_check_interval
    PictureSkill.rotation_check_interval = 2

    # Set environment variables
    os.environ["MQTT_HOST"] = mqtt_config["host"]
    os.environ["MQTT_PORT"] = str(mqtt_config["port"])
    os.environ["DEVICE_MQTT_HOST"] = mqtt_config["host"]
    os.environ["DEVICE_MQTT_PORT"] = str(mqtt_config["port"])
    os.environ["DEVICE_MQTT_USERNAME"] = ""
    os.environ["DEVICE_MQTT_PASSWORD"] = ""
    os.environ["S3_ENDPOINT"] = "localhost:9000"
    os.environ["S3_BUCKET"] = "inky-images"
    os.environ["S3_READER_ACCESS_KEY"] = ""
    os.environ["S3_READER_SECRET_KEY"] = ""

    # Start skill as background task
    skill_task = asyncio.create_task(start_skill(skill_config_file))

    # Wait for skill to initialize (less than rotation_check_interval so first check hasn't happened yet)
    await asyncio.sleep(1.5)

    yield {"next_image_id": next_image_id}

    # Cleanup
    skill_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await skill_task

    PictureSkill.rotation_check_interval = original_interval


class TestAutomaticRotation:
    """Test automatic image rotation functionality."""

    @pytest.mark.asyncio
    async def test_automatic_image_rotation(
        self,
        rotation_test_setup,
        mqtt_test_client,
    ):
        """Test that devices due for rotation automatically receive DisplayCommand.

        Flow:
        1. Device is set up with scheduled_next_at in the past
        2. Skill starts with 2-second rotation interval
        3. Rotation scheduler detects due device
        4. DisplayCommand is published to device topic
        """
        next_image_id = rotation_test_setup["next_image_id"]

        # Subscribe to device command topic
        device_command_topic = "inky/inky-test/command"
        await mqtt_test_client.subscribe(device_command_topic)

        command_received = False
        received_image_id = None
        timeout_seconds = 10  # 2s interval + buffer

        try:
            async with asyncio.timeout(timeout_seconds):
                async for message in mqtt_test_client.messages:
                    topic = str(message.topic)
                    payload = message.payload.decode()

                    if topic == device_command_topic:
                        # Parse the DisplayCommand
                        command_data = json.loads(payload)
                        assert command_data.get("action") == "display"
                        received_image_id = command_data.get("image_id")
                        command_received = True
                        logger.debug("DisplayCommand received: %s", payload)
                        break

        except TimeoutError:
            pass

        assert command_received, "Did not receive DisplayCommand within timeout"
        # The next image (never displayed) should be selected
        assert received_image_id == str(next_image_id), f"Expected image {next_image_id}, got {received_image_id}"
